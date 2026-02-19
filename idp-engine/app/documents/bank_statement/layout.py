from typing import List, Dict, Any, Tuple
from enum import Enum

class BankLayoutType(str, Enum):
    SECTION_SPLIT = "SECTION_SPLIT"          # Deposits / Withdrawals sections
    SIGNED_AMOUNT = "SIGNED_AMOUNT"          # Single table, signed values
    DUAL_COLUMN = "DUAL_COLUMN"              # Separate Debit / Credit columns
    UNKNOWN = "UNKNOWN"


class BankLayoutAnalyzer:
    """
    Responsible for:
        1. Detecting bank statement layout type
        2. Extracting raw transaction candidate rows
        3. Removing footer / summary / noise blocks

    This module does NOT normalize debit/credit.
    It only returns cleaned transaction candidate lines.
    """

    FOOTER_ANCHORS = [
        "page ",
        "important messages",
        "this page intentionally left blank",
    ]

    SUMMARY_ANCHORS = [
        "total deposits",
        "total withdrawals",
        "daily ledger balances",
    ]

    SECTION_SPLIT_ANCHORS = [
        "deposits and other credits",
        "withdrawals and other debits",
    ]

    @classmethod
    def detect_layout(cls, lines: List[Dict[str, Any]]) -> BankLayoutType:
        text_blob = " ".join([l.get("text", "").lower() for l in lines])

        if any(anchor in text_blob for anchor in cls.SECTION_SPLIT_ANCHORS):
            return BankLayoutType.SECTION_SPLIT

        if "debit" in text_blob and "credit" in text_blob:
            return BankLayoutType.DUAL_COLUMN

        if "amount" in text_blob:
            return BankLayoutType.SIGNED_AMOUNT

        return BankLayoutType.UNKNOWN

    @classmethod
    def extract_transaction_lines(
        cls,
        lines: List[Dict[str, Any]],
    ) -> Tuple[BankLayoutType, List[Dict[str, Any]]]:
        """
        Returns:
            (layout_type, contextual_transaction_candidate_lines)

        Each returned line will include an added key:
            "section": "CREDIT" | "DEBIT" | None
        """
        layout_type = cls.detect_layout(lines)

        filtered: List[Dict[str, Any]] = []
        stop_parsing = False
        current_section = None

        for line in lines:
            text = line.get("text", "")
            lower = text.lower()

            # Track section context for SECTION_SPLIT layouts
            if layout_type == BankLayoutType.SECTION_SPLIT:
                if "deposits and other credits" in lower:
                    current_section = "CREDIT"
                    continue
                if "withdrawals and other debits" in lower:
                    current_section = "DEBIT"
                    continue

            # Stop parsing when summary section begins
            if any(anchor in lower for anchor in cls.SUMMARY_ANCHORS):
                stop_parsing = True

            if stop_parsing:
                continue

            # Skip footer lines
            if any(anchor in lower for anchor in cls.FOOTER_ANCHORS):
                continue

            # Skip obvious non-transaction headers
            if lower.strip() in ["date description amount", "date description"]:
                continue

            # Candidate transaction line heuristic:
            # starts with date-like pattern MM/DD
            if cls._is_date_prefixed(text):
                contextual_line = dict(line)
                contextual_line["section"] = current_section
                filtered.append(contextual_line)

        return layout_type, filtered

    @staticmethod
    def _is_date_prefixed(text: str) -> bool:
        """
        Very basic date detection (MM/DD or M/D).
        This will be hardened later.
        """
        text = text.strip()
        if len(text) < 4:
            return False

        if "/" not in text:
            return False

        parts = text.split()
        date_token = parts[0]

        if "/" not in date_token:
            return False

        month_day = date_token.split("/")
        if len(month_day) != 2:
            return False

        return all(part.isdigit() for part in month_day)