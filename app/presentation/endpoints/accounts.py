from typing import (
    Annotated,
    Callable,
    List,
)

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.application.commands.create_account import CreateAccountCommand
from app.application.commands.delete_account import DeleteAccountCommand
from app.application.commands.deposit_transaction import CreateDepositTransactionCommand
from app.application.commands.update_account import UpdateAccountCommand
from app.application.queries.get_account import GetAccountQuery
from app.application.queries.get_account_list import GetAccountListQuery
from app.application.queries.get_account_transaction_list import GetAccountTransactionListQuery
from app.domain.accounts.schema import AccountSchema
from app.domain.transactions.schema import DepositTransactionSchema
from app.presentation.schema.account import (
    AccountBalanceSchema,
    AccountCreateSchema,
    AccountUpdateSchema,
)
from app.presentation.schema.transaction import AccountTransactionSchema


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_account_list(
    get_account_list_query: Annotated[Callable, Depends(GetAccountListQuery)]
) -> List[AccountSchema]:
    return await get_account_list_query()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreateSchema,
    create_account_command: Annotated[Callable, Depends(CreateAccountCommand)],
) -> AccountSchema:
    return await create_account_command(account_data)


@router.patch("/{account_id}/", status_code=status.HTTP_200_OK)
async def update_account(
    account_id: int,
    account_data: AccountUpdateSchema,
    update_account_command: Annotated[Callable, Depends(UpdateAccountCommand)],
) -> AccountSchema:
    return await update_account_command(account_id, account_data)


@router.delete("/{account_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: int,
    delete_account_command: Annotated[Callable, Depends(DeleteAccountCommand)],
) -> None:
    await delete_account_command(account_id)


@router.get("/{account_id}/balance/", status_code=status.HTTP_200_OK)
async def get_account_balance(
    account_id: int, get_account_query: Annotated[Callable, Depends(GetAccountQuery)]
) -> AccountBalanceSchema:
    return await get_account_query(account_id)


@router.get("/{account_id}/transactions/", status_code=status.HTTP_200_OK)
async def get_account_transaction_list(
    account_id: int,
    get_transaction_list_query: Annotated[
        Callable, Depends(GetAccountTransactionListQuery)
    ],
) -> List[AccountTransactionSchema]:
    return await get_transaction_list_query(account_id=account_id)


@router.post("/{account_id}/deposit/", status_code=status.HTTP_200_OK)
async def deposit_to_account(
    account_id: int,
    deposit_data: DepositTransactionSchema,
    deposit_transaction_command: Annotated[
        Callable, Depends(CreateDepositTransactionCommand)
    ],
) -> AccountSchema:
    return await deposit_transaction_command(account_id, deposit_data)
