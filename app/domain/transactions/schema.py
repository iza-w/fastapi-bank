from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class DepositTransactionSchema(BaseModel):
    amount: Decimal = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)
