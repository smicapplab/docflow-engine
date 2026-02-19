

from decimal import Decimal
from typing import List

from app.models.ledger import Transaction, ReconciliationResult, StatementMetadata

class BankStatementReconciler:
    """
    Performs financial reconciliation:

        opening_balance + total_credits - total_debits = closing_balance

    This module is layout-agnostic and purely financial.
    """

    @staticmethod
    def reconcile(
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

        calculated_closing = (
            metadata.opening_balance + total_credits - total_debits
        )

        delta = calculated_closing - metadata.closing_balance

        return ReconciliationResult(
            calculated_closing=calculated_closing,
            expected_closing=metadata.closing_balance,
            delta=delta,
            valid=delta == Decimal("0.00"),
        )