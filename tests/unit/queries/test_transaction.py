from decimal import Decimal

from app.application.queries.get_transaction_list import GetTransactionListQuery
from app.domain.transactions.transaction import (
    Transaction,
    TransactionTypes,
)


async def test_account_transaction_list__returns_transactions(
    async_session, account, account_2, transaction_repository
):
    query = GetTransactionListQuery(
        transaction_repository=transaction_repository,
    )

    async with async_session.begin():
        async_session.add(
            Transaction(
                amount=Decimal("100.00"),
                type=TransactionTypes.DEPOSIT,
                to_account_id=account.id,
            )
        )
        async_session.add(
            Transaction(
                amount=Decimal("200.00"),
                type=TransactionTypes.DEPOSIT,
                to_account_id=account_2.id,
            )
        )

    query_result = await query()

    assert len(query_result) == 2
