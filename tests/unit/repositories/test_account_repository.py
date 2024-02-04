from decimal import Decimal

import pytest

from app.domain.accounts.account import Account
from app.domain.accounts.exceptions import AccountDoesNotExist
from app.infrastructure.respositories.account_repository import SQLAlchemyAccountRepository


async def test_get__raises_account_when_account_does_not_exist(async_session):
    repository = SQLAlchemyAccountRepository(session=async_session)

    with pytest.raises(AccountDoesNotExist):
        await repository.get(account_id=1)


async def test_get__returns_expected_account(async_session):
    repository = SQLAlchemyAccountRepository(session=async_session)

    async with async_session.begin():
        account = Account(name="Jenny")
        async_session.add(account)

    result = await repository.get(account_id=account.id)

    assert result == account


async def test_get_list__returns_empty_list(async_session):
    repository = SQLAlchemyAccountRepository(session=async_session)

    accounts = await repository.get_list()
    assert accounts == []


async def test_get_list__returns_expected_accounts(async_session):
    repository = SQLAlchemyAccountRepository(session=async_session)

    async with async_session.begin():
        async_session.add(Account(name="Jenny"))
        async_session.add(Account(name="John", balance=Decimal("10.00")))

    accounts = await repository.get_list()

    assert len(accounts) == 2
    assert accounts[0].name == "Jenny"
    assert accounts[1].name == "John"
    assert accounts[0].balance == Decimal("0.00")
    assert accounts[1].balance == Decimal("10.00")


async def test_add__adds_account_to_database(async_session):
    repository = SQLAlchemyAccountRepository(session=async_session)

    async with async_session.begin():
        repository.add(Account(name="Jenny"))

    accounts = await repository.get_list()

    assert len(accounts) == 1
    assert accounts[0].name == "Jenny"
    assert accounts[0].balance == Decimal("0.00")


async def test_delete__removes_account_from_database(async_session):
    repository = SQLAlchemyAccountRepository(session=async_session)

    async with async_session.begin():
        account = Account(name="Jenny")
        repository.add(account)

    accounts = await repository.get_list()
    assert len(accounts) == 1

    async with async_session.begin():
        await repository.delete(account)

    accounts = await repository.get_list()
    assert len(accounts) == 0
