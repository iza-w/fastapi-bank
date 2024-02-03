from typing import Sequence

from fastapi import Depends

from app.domain.accounts.account import Account
from app.domain.accounts.account_repository import IAccountRepository


class GetAccountListQuery:
    def __init__(self, account_repository: IAccountRepository = Depends()):
        self.account_repository = account_repository

    async def __call__(self) -> Sequence[Account]:
        return await self.account_repository.get_list()
