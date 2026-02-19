from typing import List, Dict
from app.documents.registry import DocumentType

class DocumentClassifier:
    """
    Rule-based, offline-safe document classifier.

    Classification is based on textual anchors extracted from the document.
    No external services or LLM required.
    """

    @staticmethod
    def classify(lines: List[Dict]) -> DocumentType:
        if not lines:
            return DocumentType.UNKNOWN

        text_blob = " ".join([line.get("text", "") for line in lines]).lower()

        # --- Bank Statement Heuristics ---
        if (
            "account number" in text_blob
            and "beginning balance" in text_blob
            and "ending balance" in text_blob
        ):
            return DocumentType.BANK_STATEMENT

        # --- HOI Policy Heuristics ---
        if (
            "policy number" in text_blob
            and "coverage" in text_blob
            and ("effective date" in text_blob or "expiration date" in text_blob)
        ):
            return DocumentType.HOI_POLICY

        # --- Government ID Heuristics ---
        if (
            "driver license" in text_blob
            or "identification card" in text_blob
            or "date of birth" in text_blob
        ):
            return DocumentType.ID_DOCUMENT

        return DocumentType.UNKNOWN