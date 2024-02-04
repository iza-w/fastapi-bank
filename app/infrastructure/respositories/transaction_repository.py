from typing import Sequence

from fastapi import Depends
from sqlalchemy import (
    or_,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.account import Account
from app.domain.transactions.exceptions import TransactionDoesNotExist
from app.domain.transactions.transaction import Transaction
from app.domain.transactions.transaction_repository import ITransactionRepository
from app.infrastructure.database import get_session


class SQLAlchemyTransactionRepository(ITransactionRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    def add(self, transaction: Transaction) -> None:
        """Add a transaction"""
        self.session.add(transaction)

    async def get(self, transaction_id: int) -> Transaction:
        """Get transaction by id"""
        statement = select(Transaction).where(Transaction.id == transaction_id)

        cursor = await self.session.execute(statement)
        transaction = cursor.scalar()

        if transaction is None:
            raise TransactionDoesNotExist(transaction_id)

        return transaction

    async def get_list(self) -> Sequence[Transaction]:
        """Get all transactions"""
        statement = select(Transaction)

        cursor = await self.session.execute(statement)

        return cursor.scalars().all()

    async def commit(self) -> None:
        """Commit the session"""
        await self.session.commit()

    async def delete(self, transaction: Transaction) -> None:
        """Delete a transaction"""
        await self.session.delete(transaction)

    async def get_list_by_account(self, account: Account) -> Sequence[Transaction]:
        """Get all transactions for an account"""
        statement = select(Transaction).where(
            or_(
                Transaction.to_account_id == account.id,
                Transaction.from_account_id == account.id,
            )
        )

        cursor = await self.session.execute(statement)
        return cursor.scalars().all()
