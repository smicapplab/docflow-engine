from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date
from typing import List, Optional


class StatementMetadata(BaseModel):
    bank_name: str
    account_number_masked: str

    statement_start: date
    statement_end: date

    opening_balance: Decimal
    closing_balance: Decimal

    currency: str = "PHP"


class Transaction(BaseModel):
    transaction_date: date
    description: str

    debit: Optional[Decimal] = None
    credit: Optional[Decimal] = None
    balance: Optional[Decimal] = None

    raw_text: str
    page_number: int
    line_index: int

    normalized: bool = False


class ReconciliationResult(BaseModel):
    valid: bool
    delta: Decimal
    calculated_closing: Decimal


class ConfidenceScore(BaseModel):
    overall: float = Field(ge=0.0, le=1.0)
    reconciliation_weight: float = Field(ge=0.0, le=1.0)
    structure_weight: float = Field(ge=0.0, le=1.0)


class LedgerOutput(BaseModel):
    metadata: StatementMetadata
    transactions: List[Transaction]
    reconciliation: ReconciliationResult
    confidence: ConfidenceScore