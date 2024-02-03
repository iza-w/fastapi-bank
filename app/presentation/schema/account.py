from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
)


class AccountCreateSchema(BaseModel):
    name: str


class AccountUpdateSchema(BaseModel):
    name: str


class AccountBalanceSchema(BaseModel):
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)
