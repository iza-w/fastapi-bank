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

from app.application.queries.get_account_list import GetAccountListQuery
from app.domain.accounts.schema import AccountSchema


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_account_list(
    get_account_list_query: Annotated[Callable, Depends(GetAccountListQuery)]
) -> List[AccountSchema]:
    return await get_account_list_query()
