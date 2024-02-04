from app.application.commands.update_account import UpdateAccountCommand
from app.domain.accounts.schema import AccountUpdateSchema


async def test_create_account_command__creates_account_and_returns_it(
    account_repository, account
):
    command = UpdateAccountCommand(account_repository=account_repository)

    account_data = AccountUpdateSchema(name="Jennifer")

    result = await command(account.id, account_data=account_data)

    assert result.name == account_data.name
