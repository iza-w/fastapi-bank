import logging

from fastapi import Depends

from app.domain.accounts.account import Account
from app.domain.accounts.account_repository import IAccountRepository
from app.domain.accounts.exceptions import InsufficientFoundsError
from app.domain.transactions.schema import WithdrawTransactionSchema
from app.domain.transactions.transaction import (
    Transaction,
    TransactionTypes,
)
from app.domain.transactions.transaction_repository import ITransactionRepository


logger = logging.getLogger(__name__)


class WithdrawTransactionCommand:
    def __init__(
        self,
        account_repository: IAccountRepository = Depends(),
        transaction_repository: ITransactionRepository = Depends(),
    ):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    async def __call__(
        self, account_id, withdraw_data: WithdrawTransactionSchema
    ) -> Account:
        account = await self.account_repository.get(account_id, for_update=True)

        if account.balance < withdraw_data.amount:
            raise InsufficientFoundsError(account.id)

        account.balance -= withdraw_data.amount

        transaction = Transaction(
            type=TransactionTypes.WITHDRAW,
            amount=withdraw_data.amount,
            to_account_id=account.id,
        )

        self.transaction_repository.add(transaction)

        await self.transaction_repository.commit()

        logger.info(
            f"Withdraw transaction created for account {account_id}, amount: {transaction.amount}"
        )
        return account
