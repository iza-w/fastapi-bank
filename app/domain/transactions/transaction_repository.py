from abc import (
    ABC,
    abstractmethod,
)
from typing import Sequence

from app.domain.accounts.account import Account
from app.domain.transactions.transaction import Transaction


class ITransactionRepository(ABC):
    @abstractmethod
    async def get(self, pk: int) -> Transaction:
        """Get transaction by id"""
        pass  # pragma: no cover

    @abstractmethod
    async def get_list(self) -> Sequence[Transaction]:
        """Get all accounts"""
        pass  # pragma: no cover

    @abstractmethod
    def add(self, transaction: Transaction) -> None:
        """Add a new transaction"""
        pass  # pragma: no cover

    @abstractmethod
    async def commit(self) -> None:
        """Commit the session"""
        pass  # pragma: no cover

    @abstractmethod
    async def delete(self, transaction: Transaction) -> None:
        """Delete a transaction"""
        pass  # pragma: no cover

    @abstractmethod
    async def get_list_by_account(self, account: Account) -> Sequence[Transaction]:
        """Get all transactions by account"""
        pass  # pragma: no cover
