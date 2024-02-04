from app.application.commands.delete_account import DeleteAccountCommand
from app.domain.accounts.account import Account


async def test_delete_account_command__deletes_account(
    async_session, account_repository
):
    command = DeleteAccountCommand(account_repository=account_repository)

    async with async_session.begin():
        account = Account(name="Jenny")
        async_session.add(account)

    await command(account_id=account.id)

    accounts = await account_repository.get_list()
    assert len(accounts) == 0
