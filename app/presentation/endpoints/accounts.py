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
from app.application.queries.get_account_list import GetAccountListQuery
from app.domain.accounts.schema import AccountSchema
from app.presentation.schema.account import AccountCreateSchema


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
