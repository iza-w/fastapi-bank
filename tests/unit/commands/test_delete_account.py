from app.application.commands.delete_account import DeleteAccountCommand
from app.domain.accounts.account import Account
from app.infrastructure.respositories.account_repository import SQLAlchemyAccountRepository


async def test_delete_account_command__deletes_account(
    async_session,
):
    account_repository = SQLAlchemyAccountRepository(session=async_session)
    command = DeleteAccountCommand(account_repository=account_repository)

    async with async_session.begin():
        account = Account(name="Jenny")
        async_session.add(account)

    await command(account_id=account.id)

    accounts = await account_repository.get_list()
    assert len(accounts) == 0
