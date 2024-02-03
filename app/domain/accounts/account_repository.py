from abc import (
    ABC,
    abstractmethod,
)
from typing import Sequence

from app.domain.accounts.account import Account


class IAccountRepository(ABC):
    @abstractmethod
    async def get(self, pk: int, for_update: bool = False) -> Account:
        """Get account by id"""
        pass  # pragma: no cover

    @abstractmethod
    async def get_list(self) -> Sequence[Account]:
        """Get all accounts"""
        pass  # pragma: no cover

    @abstractmethod
    def add(self, account: Account) -> None:
        """Add a new account"""
        pass  # pragma: no cover

    @abstractmethod
    async def commit(self) -> None:
        """Commit the session"""
        pass  # pragma: no cover

    @abstractmethod
    async def delete(self, account: Account) -> None:
        """Delete an account"""
        pass  # pragma: no cover
