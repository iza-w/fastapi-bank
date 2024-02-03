import logging

from fastapi import Depends

from app.domain.accounts.account_repository import IAccountRepository


logger = logging.getLogger(__name__)


class DeleteAccountCommand:
    def __init__(self, account_repository: IAccountRepository = Depends()):
        self.account_repository = account_repository

    async def __call__(self, account_id: int) -> None:
        account = await self.account_repository.get(account_id)

        await self.account_repository.delete(account)
        await self.account_repository.commit()

        logger.info(f"Account with {account_id} has been deleted.")
