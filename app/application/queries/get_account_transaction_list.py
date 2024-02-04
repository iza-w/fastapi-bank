from typing import Sequence

from fastapi import Depends

from app.domain.accounts.account_repository import IAccountRepository
from app.domain.transactions.transaction import Transaction
from app.domain.transactions.transaction_repository import ITransactionRepository


class GetAccountTransactionListQuery:
    def __init__(
        self,
        transaction_repository: ITransactionRepository = Depends(),
        account_repository: IAccountRepository = Depends(),
    ):
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository

    async def __call__(self, account_id: int) -> Sequence[Transaction]:
        account = await self.account_repository.get(account_id)
        return await self.transaction_repository.get_list_by_account(account)
