from datetime import datetime
from decimal import Decimal

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
