import logging

from fastapi import Depends

from app.domain.accounts.account import Account
from app.domain.accounts.account_repository import IAccountRepository
from app.domain.accounts.schema import AccountCreateSchema


logger = logging.getLogger(__name__)


class CreateAccountCommand:
    def __init__(self, account_repository: IAccountRepository = Depends()):
        self.account_repository = account_repository

    async def __call__(self, account_data: AccountCreateSchema) -> Account:
        logger.info(f"Creating a new account: {account_data}")

        account = Account(**account_data.model_dump())

        self.account_repository.add(account)
        await self.account_repository.commit()

        logger.info(f"Account created successfully: {account}")
        return account
