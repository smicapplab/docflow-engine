from typing import Any
from app.core.extractor import PDFTextExtractor
from app.core.classifier import DocumentClassifier
from app.documents.registry import resolve_parser, DocumentType

class DocumentRouter:
    """
    Orchestrates the full document processing pipeline:

    1) Extract raw lines
    2) Classify document type
    3) Resolve appropriate parser
    4) Execute parsing
    5) Return structured model
    """

    def __init__(self):
        self.extractor = PDFTextExtractor()

    def process(self, pdf_path: str) -> Any:
        # Step 1: Extract raw lines
        lines = self.extractor.extract_lines(pdf_path)

        # Step 2: Classify document type
        doc_type = DocumentClassifier.classify(lines)

        if doc_type == DocumentType.UNKNOWN:
            raise ValueError("Unsupported or unrecognized document type.")

        # Step 3: Resolve parser
        parser_cls = resolve_parser(doc_type)

        # Step 4: Instantiate and parse
        parser = parser_cls(lines)
        result = parser.parse()

        return result