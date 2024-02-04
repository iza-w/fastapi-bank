from typing import Sequence

from fastapi import Depends

from app.domain.transactions.transaction import Transaction
from app.domain.transactions.transaction_repository import ITransactionRepository


class GetTransactionListQuery:
    def __init__(self, transaction_repository: ITransactionRepository = Depends()):
        self.transaction_repository = transaction_repository

    async def __call__(self) -> Sequence[Transaction]:
        return await self.transaction_repository.get_list()
