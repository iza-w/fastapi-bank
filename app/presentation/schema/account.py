from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
)


class AccountBalanceSchema(BaseModel):
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)
