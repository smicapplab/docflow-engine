import logging
import pdfplumber
from app.models.ledger import LedgerOutput

logger = logging.getLogger(__name__)


class BankAExtractor:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> LedgerOutput:
        if not self._has_text_layer():
            raise NotImplementedError("OCR path not implemented yet.")

        raw_lines = self._extract_raw_lines()
        metadata = self._parse_metadata(raw_lines)
        transactions = self._parse_transactions(raw_lines)
        reconciliation = self._reconcile(metadata, transactions)
        confidence = self._compute_confidence(reconciliation)

        return LedgerOutput(
            metadata=metadata,
            transactions=transactions,
            reconciliation=reconciliation,
            confidence=confidence
        )

    def _extract_raw_lines(self):
        """
        Extract raw text lines from a digital-native PDF.
        Returns a list of dicts:
        {
            "page_number": int,
            "line_index": int,
            "text": str
        }
        """
        extracted = []

        with pdfplumber.open(self.file_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()

                if not text:
                    continue

                lines = text.split("\n")

                for line_index, line in enumerate(lines):
                    cleaned = line.strip()
                    if not cleaned:
                        continue

                    extracted.append(
                        {
                            "page_number": page_number,
                            "line_index": line_index,
                            "text": cleaned,
                        }
                    )

                    # Debug output for inspection
                    logger.debug(f"[Page {page_number}][Line {line_index}] {cleaned}")

        return extracted

    def _has_text_layer(self) -> bool:
        """
        Detect whether the PDF contains an embedded text layer.
        Returns True if at least one page contains extractable text.
        """
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    return True
        return False

    def _parse_metadata(self, lines):
        raise NotImplementedError("Metadata parsing not implemented yet.")

    def _parse_transactions(self, lines):
        raise NotImplementedError("Transaction parsing not implemented yet.")

    def _reconcile(self, metadata, transactions):
        raise NotImplementedError("Reconciliation not implemented yet.")

    def _compute_confidence(self, reconciliation):
        raise NotImplementedError("Confidence scoring not implemented yet.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bank_a.py <pdf_path>")
        sys.exit(1)

    logging.basicConfig(level=logging.DEBUG)
    extractor = BankAExtractor(sys.argv[1])
    extractor._extract_raw_lines()