from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.account import Account
from app.domain.accounts.account_repository import IAccountRepository
from app.domain.accounts.exceptions import AccountDoesNotExist
from app.infrastructure.database import get_session


class SQLAlchemyAccountRepository(IAccountRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    def add(self, account: Account) -> None:
        """Add an account."""
        self.session.add(account)

    async def get(self, account_id: int, for_update: bool = False) -> Account:
        """Get an account by account_id."""
        statement = select(Account).where(Account.id == account_id)
        if for_update:
            statement = statement.with_for_update()

        cursor = await self.session.execute(statement)
        account = cursor.scalar()

        if account is None:
            raise AccountDoesNotExist(account_id)
        return account

    async def get_list(self) -> Sequence[Account]:
        """Get a list of accounts."""
        stmt = select(Account)

        async with self.session.begin():
            cursor = await self.session.execute(stmt)
            return cursor.scalars().all()

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self.session.commit()

    async def delete(self, account: Account) -> None:
        """Delete an account."""
        await self.session.delete(account)
