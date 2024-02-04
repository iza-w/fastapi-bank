from datetime import datetime
from decimal import Decimal

from starlette import status

from app.domain.accounts.account import Account
from app.domain.transactions.transaction import (
    Transaction,
    TransactionTypes,
)


async def test_account_transaction_list__returns_expected_transactions(
    app, async_client, async_session
):
    account = Account(name="Jenny")

    transaction = Transaction(
        to_account=account,
        amount=Decimal("100.00"),
        type=TransactionTypes.DEPOSIT,
        created_at=datetime(2021, 1, 1),
    )
    transaction_2 = Transaction(
        from_account=account,
        amount=Decimal("50.00"),
        type=TransactionTypes.WITHDRAW,
        created_at=datetime(2021, 1, 2),
    )

    async with async_session.begin():
        async_session.add(account)
        async_session.add(transaction)
        async_session.add(transaction_2)

    response = await async_client.get(
        app.url_path_for("get_account_transaction_list", account_id=account.id)
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "amount": "100.00",
            "type": "deposit",
            "created_at": "2021-01-01T00:00:00",
        },
        {
            "id": 2,
            "amount": "50.00",
            "type": "withdraw",
            "created_at": "2021-01-02T00:00:00",
        },
    ]
