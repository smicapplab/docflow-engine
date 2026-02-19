from typing import Type, Dict
from enum import Enum
from app.documents.base import BaseDocumentParser

class DocumentType(str, Enum):
    """
    Supported high-level document types.
    Extend this enum as new document types are introduced.
    """
    BANK_STATEMENT = "BANK_STATEMENT"
    HOI_POLICY = "HOI_POLICY"
    ID_DOCUMENT = "ID_DOCUMENT"
    UNKNOWN = "UNKNOWN"


# Import parsers lazily inside factory to avoid circular imports


def get_document_registry() -> Dict[DocumentType, Type[BaseDocumentParser]]:
    """
    Returns mapping of document type → parser class.
    Import statements are kept inside this function to prevent circular imports.
    """
    from app.documents.bank_statement.parser import BankStatementParser
    from app.documents.hoi.parser import HOIParser
    from app.documents.id_document.parser import IDDocumentParser

    return {
        DocumentType.BANK_STATEMENT: BankStatementParser,
        DocumentType.HOI_POLICY: HOIParser,
        DocumentType.ID_DOCUMENT: IDDocumentParser,
    }


def resolve_parser(doc_type: DocumentType) -> Type[BaseDocumentParser]:
    """
    Resolve parser class for given document type.
    Raises ValueError if unsupported.
    """
    registry = get_document_registry()

    if doc_type not in registry:
        raise ValueError(f"Unsupported document type: {doc_type}")

    return registry[doc_type]