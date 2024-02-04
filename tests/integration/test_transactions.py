from datetime import datetime
from decimal import Decimal

from starlette import status

from app.domain.accounts.account import Account
from app.domain.transactions.transaction import (
    Transaction,
    TransactionTypes,
)


async def test_get_transaction_list_with_no_transactions__returns_empty_list(
    app, async_client
):
    response = await async_client.get(app.url_path_for("get_transaction_list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_get_transaction_list__returns_expected_transactions(
    app, async_client, async_session
):
    account = Account(name="Jenny")

    transaction_1 = Transaction(
        amount=Decimal("100.00"),
        type=TransactionTypes.DEPOSIT,
        to_account=account,
        created_at=datetime(2021, 1, 1),
    )
    transaction_2 = Transaction(
        amount=Decimal("200.00"),
        type=TransactionTypes.WITHDRAW,
        from_account=account,
        created_at=datetime(2022, 1, 1),
    )

    async with async_session.begin():
        async_session.add(transaction_1)
        async_session.add(transaction_2)

    response = await async_client.get(app.url_path_for("get_transaction_list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "amount": "100.00",
            "type": "deposit",
            "from_account_id": None,
            "to_account_id": 1,
            "created_at": "2021-01-01T00:00:00",
        },
        {
            "id": 2,
            "amount": "200.00",
            "type": "withdraw",
            "from_account_id": 1,
            "to_account_id": None,
            "created_at": "2022-01-01T00:00:00",
        },
    ]
