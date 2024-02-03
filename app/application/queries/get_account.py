from typing import Sequence

from fastapi import Depends

from app.domain.accounts.account import Account
from app.domain.accounts.account_repository import IAccountRepository


class GetAccountQuery:
    def __init__(self, account_repository: IAccountRepository = Depends()):
        self.account_repository = account_repository

    async def __call__(self, account_id: int) -> Sequence[Account]:
        return await self.account_repository.get(account_id)
