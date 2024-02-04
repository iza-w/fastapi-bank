from decimal import Decimal

import pytest

from app.domain.accounts.account import Account
from app.domain.transactions.exceptions import TransactionDoesNotExist
from app.domain.transactions.transaction import (
    Transaction,
    TransactionTypes,
)
from app.infrastructure.respositories.transaction_repository import SQLAlchemyTransactionRepository


async def test_get__raises_transaction_does_not_exist(async_session):
    repository = SQLAlchemyTransactionRepository(session=async_session)

    with pytest.raises(TransactionDoesNotExist):
        await repository.get(transaction_id=1)


async def test_get__returns_expected_transaction(async_session):
    repository = SQLAlchemyTransactionRepository(session=async_session)

    async with async_session.begin():
        async_session.add(Account(id=1, name="Jenny"))

    async with async_session.begin():
        transaction = Transaction(
            amount=Decimal("100.00"), type=TransactionTypes.DEPOSIT, to_account_id=1
        )
        async_session.add(transaction)

    result = await repository.get(transaction_id=transaction.id)

    assert result == transaction


async def test_get_list__returns_expected_transactions(async_session):
    repository = SQLAlchemyTransactionRepository(session=async_session)

    async with async_session.begin():
        account = Account(id=1, name="Jenny")
        async_session.add(account)

        transaction = Transaction(
            amount=Decimal("100.00"), type=TransactionTypes.DEPOSIT, to_account_id=1
        )
        transaction_2 = Transaction(
            amount=Decimal("50.00"), type=TransactionTypes.DEPOSIT, from_account_id=1
        )
        async_session.add(transaction)
        async_session.add(transaction_2)

    result = await repository.get_list()

    assert result == [transaction, transaction_2]


async def test_get_list_by_account__returns_expected_transactions(async_session):
    repository = SQLAlchemyTransactionRepository(session=async_session)
    account = Account(id=1, name="Jenny")

    async with async_session.begin():
        async_session.add(account)

        transaction = Transaction(
            amount=Decimal("100.00"), type=TransactionTypes.DEPOSIT, to_account_id=1
        )
        transaction_2 = Transaction(
            amount=Decimal("50.00"), type=TransactionTypes.DEPOSIT, from_account_id=1
        )
        async_session.add(transaction)
        async_session.add(transaction_2)

    result = await repository.get_list_by_account(account=account)

    assert result == [transaction, transaction_2]


async def test_delete__deletes_transaction(async_session):
    repository = SQLAlchemyTransactionRepository(session=async_session)

    async with async_session.begin():
        async_session.add(Account(id=1, name="Jenny"))
        transaction = Transaction(
            amount=Decimal("100.00"), type=TransactionTypes.DEPOSIT, to_account_id=1
        )
        async_session.add(transaction)

    async with async_session.begin():
        await repository.delete(transaction=transaction)

    transactions = await repository.get_list()
    assert len(transactions) == 0
