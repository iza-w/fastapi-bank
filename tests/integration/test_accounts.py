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


async def test_create_account__should_return_account_with_zero_balance(
    app, async_client
):
    response = await async_client.post(
        app.url_path_for("get_account_list"), json={"name": "Jenny"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 1, "name": "Jenny", "balance": "0.00"}


async def test_create_account__with_invalid_data_returns_bad_request(app, async_client):
    response = await async_client.post(app.url_path_for("get_account_list"), json={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()

    assert data["detail"] == [
        {
            "type": "missing",
            "loc": ["body", "name"],
            "msg": "Field required",
            "input": {},
            "url": "https://errors.pydantic.dev/2.6/v/missing",
        },
    ]
