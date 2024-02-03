from pydantic import BaseModel


class AccountCreateSchema(BaseModel):
    name: str
