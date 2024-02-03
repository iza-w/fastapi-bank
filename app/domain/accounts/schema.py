from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
)


class AccountSchema(BaseModel):
    id: int
    name: str
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)
