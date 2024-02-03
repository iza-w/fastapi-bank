from pydantic import BaseModel


class AccountCreateSchema(BaseModel):
    name: str


class AccountUpdateSchema(BaseModel):
    name: str
