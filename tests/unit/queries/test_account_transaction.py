from decimal import Decimal

from app.application.queries.get_account_transaction_list import GetAccountTransactionListQuery
from app.domain.transactions.transaction import (
    Transaction,
    TransactionTypes,
)


async def test_account_transaction_list__returns_transactions(
    async_session, account, account_repository, transaction_repository
):
    query = GetAccountTransactionListQuery(
        account_repository=account_repository,
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
                amount=Decimal("150.00"),
                type=TransactionTypes.DEPOSIT,
                to_account_id=account.id,
            )
        )

    query_result = await query(account.id)

    assert len(query_result) == 2
