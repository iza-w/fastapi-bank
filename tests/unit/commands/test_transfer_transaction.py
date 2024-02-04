from decimal import Decimal

import pytest

from app.application.commands.transfer_transaction import TransferTransactionCommand
from app.domain.accounts.exceptions import InsufficientFoundsError
from app.domain.transactions.schema import TransferTransactionSchema


async def test_transfer__transfers_between_accounts_and_returns_updated_accounts(
    account, account_2, account_repository, transaction_repository
):
    command = TransferTransactionCommand(
        account_repository=account_repository,
        transaction_repository=transaction_repository,
    )

    transfer_data = TransferTransactionSchema(
        amount=Decimal("50.00"), to_account_id=account_2.id
    )
    result = await command(account.id, transfer_data)

    assert result.balance == Decimal("50.00")

    recipient = await account_repository.get(account_2.id)
    assert recipient.balance == Decimal("150.00")


async def test_transfer__raises_insufficient_funds_error(
    account, account_2, account_repository, transaction_repository
):
    command = TransferTransactionCommand(
        account_repository=account_repository,
        transaction_repository=transaction_repository,
    )

    transfer_data = TransferTransactionSchema(
        amount=Decimal("150.00"), to_account_id=account_2.id
    )

    with pytest.raises(InsufficientFoundsError):
        await command(account.id, transfer_data)
