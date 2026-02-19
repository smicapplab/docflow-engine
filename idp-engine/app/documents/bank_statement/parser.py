from typing import List, Dict, Any
from decimal import Decimal
from datetime import datetime
from app.documents.base import BaseDocumentParser

from app.models.ledger import (
    LedgerOutput,
    StatementMetadata,
    Transaction,
    ReconciliationResult,
)

class BankStatementParser(BaseDocumentParser):
    """
    Minimal working Bank Statement parser.

    This is a transitional implementation to restore
    end-to-end functionality under the new architecture.
    Logic will later be split into:
        - layout
        - normalizer
        - reconciler
    """

    def parse(self) -> LedgerOutput:
        metadata = self._parse_metadata(self.lines)
        transactions = self._parse_transactions(self.lines)
        reconciliation = self._reconcile(metadata, transactions)

        return LedgerOutput(
            metadata=metadata,
            transactions=transactions,
            reconciliation=reconciliation,
            confidence=0.5,  # temporary static confidence
        )

    # -----------------------------------------------------
    # Temporary Inline Logic (will refactor later)
    # -----------------------------------------------------

    def _parse_metadata(self, lines: List[Dict[str, Any]]) -> StatementMetadata:
        text_blob = " ".join([l.get("text", "") for l in lines])

        # Extremely simple heuristics (placeholder)
        institution = "Unknown Institution"
        account_holder = "Unknown"
        account_number = None
        opening_balance = Decimal("0.00")
        closing_balance = Decimal("0.00")

        for line in lines:
            text = line.get("text", "")

            if "Bank of" in text:
                institution = text.strip()

            if "Beginning balance" in text:
                try:
                    opening_balance = Decimal(text.split()[-1].replace(",", ""))
                except Exception:
                    pass

            if "Ending balance" in text:
                try:
                    closing_balance = Decimal(text.split()[-1].replace(",", ""))
                except Exception:
                    pass

        return StatementMetadata(
            institution=institution,
            account_holder=account_holder,
            account_number=account_number,
            statement_start=None,
            statement_end=None,
            opening_balance=opening_balance,
            closing_balance=closing_balance,
            currency="USD",
        )

    def _parse_transactions(self, lines: List[Dict[str, Any]]) -> List[Transaction]:
        transactions: List[Transaction] = []

        for line in lines:
            text = line.get("text", "")

            # Very naive date-based detection (MM/DD)
            if len(text) >= 5 and text[2] == "/":
                parts = text.split()
                try:
                    date = datetime.strptime(parts[0], "%m/%d").replace(year=datetime.now().year)
                except Exception:
                    continue

                amount = None
                for token in reversed(parts):
                    try:
                        amount = Decimal(token.replace(",", ""))
                        break
                    except Exception:
                        continue

                if amount is None:
                    continue

                transactions.append(
                    Transaction(
                        date=date.date(),
                        description=" ".join(parts[1:-1]),
                        debit=amount if amount < 0 else None,
                        credit=amount if amount > 0 else None,
                        balance=None,
                        normalized=False,
                    )
                )

        return transactions

    def _reconcile(
        self,
        metadata: StatementMetadata,
        transactions: List[Transaction],
    ) -> ReconciliationResult:
        total_credits = Decimal("0.00")
        total_debits = Decimal("0.00")

        for tx in transactions:
            if tx.credit:
                total_credits += tx.credit
            if tx.debit:
                total_debits += tx.debit

        calculated = metadata.opening_balance + total_credits - total_debits
        delta = calculated - metadata.closing_balance

        return ReconciliationResult(
            calculated_closing=calculated,
            expected_closing=metadata.closing_balance,
            delta=delta,
            valid=delta == Decimal("0.00"),
        )
