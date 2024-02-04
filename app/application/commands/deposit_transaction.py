import logging

from fastapi import Depends

from app.domain.accounts.account import Account
from app.domain.accounts.account_repository import IAccountRepository
from app.domain.transactions.schema import DepositTransactionSchema
from app.domain.transactions.transaction import (
    Transaction,
    TransactionTypes,
)
from app.domain.transactions.transaction_repository import ITransactionRepository


logger = logging.getLogger(__name__)


class DepositTransactionCommand:
    def __init__(
        self,
        account_repository: IAccountRepository = Depends(),
        transaction_repository: ITransactionRepository = Depends(),
    ):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    async def __call__(
        self, account_id: int, deposit_data: DepositTransactionSchema
    ) -> Account:
        account = await self.account_repository.get(account_id, for_update=True)
        account.balance += deposit_data.amount

        transaction = Transaction(
            to_account_id=account.id,
            type=TransactionTypes.DEPOSIT,
            amount=deposit_data.amount,
        )
        self.transaction_repository.add(transaction)
        await self.transaction_repository.commit()

        logger.info(
            f"Deposit transaction created for account {account_id}, amount: {transaction.amount}"
        )
        return account
