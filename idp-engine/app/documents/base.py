from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseDocumentParser(ABC):
    """
    Base interface for all document parsers.

    Every document type (Bank Statement, HOI, ID, etc.) must implement this contract.
    Parsers operate on extracted raw lines and return a structured model.
    """

    def __init__(self, lines: List[Dict[str, Any]]):
        self.lines = lines

    @abstractmethod
    def parse(self):
        """
        Parse extracted lines into a structured Pydantic model.

        Must return a document-specific structured model.
        """
        raise NotImplementedError