from typing import List, Dict, Any
from decimal import Decimal
from datetime import datetime

from app.documents.bank_statement.layout import BankLayoutType
from app.models.ledger import Transaction

class BankTransactionNormalizer:
    """
    Responsible for converting layout-specific transaction lines
    into normalized Transaction models.

    This layer:
        - Extracts amount
        - Determines debit / credit
        - Cleans description
        - Leaves reconciliation to reconciler module
    """

    @staticmethod
    def normalize(
        layout_type: BankLayoutType,
        candidate_lines: List[Dict[str, Any]],
    ) -> List[Transaction]:
        transactions: List[Transaction] = []

        current_section = None  # Used for SECTION_SPLIT layouts

        for line in candidate_lines:
            text = line.get("text", "")
            lower = text.lower()

            # SECTION tracking (for split layouts)
            if layout_type == BankLayoutType.SECTION_SPLIT:
                if "deposits and other credits" in lower:
                    current_section = "CREDIT"
                    continue
                if "withdrawals and other debits" in lower:
                    current_section = "DEBIT"
                    continue

            parts = text.split()
            if not parts:
                continue

            # ---- Date Parsing ----
            try:
                date = datetime.strptime(parts[0], "%m/%d")
                date = date.replace(year=datetime.now().year).date()
            except Exception:
                continue

            # ---- Amount Extraction ----
            amount = None
            for token in reversed(parts):
                cleaned = token.replace(",", "")
                try:
                    amount = Decimal(cleaned)
                    break
                except Exception:
                    continue

            if amount is None:
                continue

            debit = None
            credit = None

            # ---- Layout-based Normalization ----
            if layout_type == BankLayoutType.SECTION_SPLIT:
                if current_section == "CREDIT":
                    credit = abs(amount)
                elif current_section == "DEBIT":
                    debit = abs(amount)

            elif layout_type == BankLayoutType.SIGNED_AMOUNT:
                if amount < 0:
                    debit = abs(amount)
                else:
                    credit = abs(amount)

            elif layout_type == BankLayoutType.DUAL_COLUMN:
                # Placeholder: treat signed until column detection added
                if amount < 0:
                    debit = abs(amount)
                else:
                    credit = abs(amount)

            # ---- Description Cleanup ----
            description = " ".join(parts[1:-1]).strip()

            transactions.append(
                Transaction(
                    date=date,
                    description=description,
                    debit=debit,
                    credit=credit,
                    balance=None,
                    normalized=True,
                )
            )

        return transactions