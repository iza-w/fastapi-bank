"""empty message

Revision ID: c5bf472fcfa5
Revises:
Create Date: 2024-02-03 15:16:25.189483

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c5bf472fcfa5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum("DEPOSIT", "WITHDRAW", "TRANSFER", name="transactiontypes").create(
        op.get_bind()
    )
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("balance", sa.DECIMAL(precision=12, scale=2), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_accounts_id"), "accounts", ["id"], unique=False)
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            postgresql.ENUM(
                "DEPOSIT",
                "WITHDRAW",
                "TRANSFER",
                name="transactiontypes",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("amount", sa.DECIMAL(precision=12, scale=2), nullable=False),
        sa.Column("from_account_id", sa.Integer(), nullable=True),
        sa.Column("to_account_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["from_account_id"],
            ["accounts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["to_account_id"],
            ["accounts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_transactions_id"), "transactions", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_transactions_id"), table_name="transactions")
    op.drop_table("transactions")
    op.drop_index(op.f("ix_accounts_id"), table_name="accounts")
    op.drop_table("accounts")
    sa.Enum("DEPOSIT", "WITHDRAW", "TRANSFER", name="transactiontypes").drop(
        op.get_bind()
    )
    # ### end Alembic commands ###