import pytest

from app.application.commands.withdraw_transaction import WithdrawTransactionCommand
from app.domain.accounts.account import Account
from app.domain.accounts.exceptions import InsufficientFoundsError
from app.domain.transactions.schema import WithdrawTransactionSchema
from app.infrastructure.respositories.account_repository import SQLAlchemyAccountRepository
from app.infrastructure.respositories.transaction_repository import SQLAlchemyTransactionRepository

from decimal import Decimal


async def test_withdraw_from_account__returns_updated_account(
    async_session, account_repository, transaction_repository
):
    command = WithdrawTransactionCommand(account_repository=account_repository,
                                         transaction_repository=transaction_repository)

    account = Account(name="Jenny", balance=Decimal("100.00"))

    async with async_session.begin():
        async_session.add(account)

    withdraw_data = WithdrawTransactionSchema(amount=Decimal("50.00"))
    command_result = await command(account_id=account.id, withdraw_data=withdraw_data)

    assert command_result.balance == Decimal("50.00")


async def test_withdraw_from_account__raises_insufficient_founds_error(
    async_session, account_repository, transaction_repository
):
    command = WithdrawTransactionCommand(account_repository=account_repository,
                                         transaction_repository=transaction_repository)

    account = Account(name="Jenny", balance=Decimal("100.00"))

    async with async_session.begin():
        async_session.add(account)

    withdraw_data = WithdrawTransactionSchema(amount=Decimal("150.00"))

    with pytest.raises(InsufficientFoundsError):
        await command(account_id=account.id, withdraw_data=withdraw_data)
