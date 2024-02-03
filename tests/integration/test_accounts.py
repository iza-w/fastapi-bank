from starlette import status

from app.domain.accounts.account import Account


async def test_account_list__should_return_expected_accounts(
    app, async_client, async_session
):
    async with async_session.begin():
        async_session.add(Account(name="Jenny"))
        async_session.add(Account(name="John"))

    response = await async_client.get(app.url_path_for("get_account_list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "name": "Jenny", "balance": "0.00"},
        {"id": 2, "name": "John", "balance": "0.00"},
    ]
