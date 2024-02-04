from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.domain.transactions.transaction import TransactionTypes


class AccountTransactionSchema(BaseModel):
    id: int
    amount: Decimal
    type: TransactionTypes
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionSchema(BaseModel):
    id: int
    amount: Decimal
    type: TransactionTypes
    created_at: datetime

    from_account_id: Optional[int]
    to_account_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)
