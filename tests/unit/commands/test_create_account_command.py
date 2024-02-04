from decimal import Decimal

from app.application.commands.create_account import CreateAccountCommand
from app.domain.accounts.schema import AccountCreateSchema


async def test_create_account_command__creates_account_and_returns_it(
    account_repository
):
    command = CreateAccountCommand(account_repository=account_repository)

    account_data = AccountCreateSchema(name="Jenny")

    result = await command(account_data=account_data)

    assert result.name == "Jenny"
    assert result.balance == Decimal("0.00")
