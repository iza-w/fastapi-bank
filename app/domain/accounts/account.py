from decimal import Decimal

from sqlalchemy import DECIMAL
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.infrastructure.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    balance: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=12, scale=2), default=Decimal("0.00")
    )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f"{self.id}: {self.name}"
