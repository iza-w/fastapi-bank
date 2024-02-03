import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DECIMAL,
    DateTime,
    Enum,
    ForeignKey,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.domain.accounts.account import Account
from app.infrastructure.database import Base


class TransactionTypes(enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    type: Mapped[TransactionTypes] = mapped_column(Enum(TransactionTypes))
    amount: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=12, scale=2), default=Decimal("0.00")
    )

    from_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=True
    )
    to_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=True)

    from_account: Mapped[Account] = relationship(
        "Account", foreign_keys=[from_account_id]
    )
    to_account: Mapped[Account] = relationship(
        "Account", foreign_keys=[to_account_id], cascade="all"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
