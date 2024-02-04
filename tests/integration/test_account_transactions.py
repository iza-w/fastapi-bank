from datetime import datetime
from decimal import Decimal

import pytest
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


@pytest.mark.parametrize(
    "amount, expected_status, expected_response",
    [
        ("100.00", status.HTTP_200_OK, {"id": 1, "name": "Jenny", "balance": "150.00"}),
        (
            "-100.00",
            status.HTTP_400_BAD_REQUEST,
            {
                "detail": [
                    {
                        "type": "greater_than",
                        "loc": ["body", "amount"],
                        "msg": "Input should be greater than 0",
                        "input": "-100.00",
                        "ctx": {"gt": 0},
                    }
                ],
            },
        ),
    ],
)
async def test_deposit_to_account__returns_updated_account(
    app, async_client, async_session, amount, expected_status, expected_response
):
    account = Account(name="Jenny", balance=Decimal("50.00"))

    async with async_session.begin():
        async_session.add(account)

    response = await async_client.post(
        app.url_path_for("deposit_to_account", account_id=account.id),
        json={"amount": amount},
    )

    assert response.status_code == expected_status
    assert response.json() == expected_response
