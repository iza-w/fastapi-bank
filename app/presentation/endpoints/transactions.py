import logging
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

from app.application.queries.get_transaction_list import GetTransactionListQuery
from app.presentation.schema.transaction import TransactionSchema


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_transaction_list(
    get_transaction_list_query: Annotated[Callable, Depends(GetTransactionListQuery)]
) -> List[TransactionSchema]:
    """Get a list of transactions."""
    return await get_transaction_list_query()
