from decimal import Decimal

from app.application.commands.deposit_transaction import DepositTransactionCommand
from app.domain.transactions.schema import DepositTransactionSchema


async def test_deposit__deposits_to_account_and_returns_updated_account(
    account, account_repository, transaction_repository
):
    command = DepositTransactionCommand(
        account_repository=account_repository,
        transaction_repository=transaction_repository,
    )

    deposit_data = DepositTransactionSchema(amount=Decimal("100.00"))
    result = await command(account.id, deposit_data)

    assert result.balance == Decimal("200.00")
