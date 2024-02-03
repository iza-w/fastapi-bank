import logging

from fastapi import Depends

from app.domain.accounts.account import Account
from app.domain.accounts.account_repository import IAccountRepository
from app.presentation.schema.account import AccountUpdateSchema


logger = logging.getLogger(__name__)


class UpdateAccountCommand:
    def __init__(self, account_repository: IAccountRepository = Depends()):
        self.account_repository = account_repository

    async def __call__(
        self, account_id: int, account_data: AccountUpdateSchema
    ) -> Account:
        logger.info(f"Update an account({account_id}) with data: {account_data}")

        account = await self.account_repository.get(account_id)
        account.update(**account_data.model_dump())

        await self.account_repository.commit()

        logger.info(f"Updated account with id: {account_id}")
        return account
