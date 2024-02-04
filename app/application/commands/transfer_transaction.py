import logging

from fastapi import Depends

from app.domain.accounts.account import Account
from app.domain.accounts.account_repository import IAccountRepository
from app.domain.accounts.exceptions import InsufficientFoundsError
from app.domain.transactions.schema import TransferTransactionSchema
from app.domain.transactions.transaction import (
    Transaction,
    TransactionTypes,
)
from app.domain.transactions.transaction_repository import ITransactionRepository


logger = logging.getLogger(__name__)


class CreateTransferTransactionCommand:
    def __init__(
        self,
        account_repository: IAccountRepository = Depends(),
        transaction_repository: ITransactionRepository = Depends(),
    ):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    async def __call__(
        self, account_id: int, transfer_data: TransferTransactionSchema
    ) -> Account:
        from_account = await self.account_repository.get(account_id, for_update=True)
        to_account = await self.account_repository.get(
            transfer_data.to_account_id, for_update=True
        )

        if from_account.balance < transfer_data.amount:
            raise InsufficientFoundsError(from_account.id)

        from_account.balance -= transfer_data.amount
        to_account.balance += transfer_data.amount

        transaction = Transaction(
            type=TransactionTypes.WITHDRAW,
            amount=transfer_data.amount,
            from_account_id=from_account.id,
            to_account_id=to_account.id,
        )
        self.transaction_repository.add(transaction)
        await self.transaction_repository.commit()

        logger.info(
            f"Transfer transaction created from account {from_account.id} to account {to_account.id}, "
            f"amount: {transaction.amount}"
        )
        return from_account
