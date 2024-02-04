from decimal import Decimal
import pytest

from app.domain.accounts.account import Account
from app.infrastructure.respositories.account_repository import SQLAlchemyAccountRepository
from app.infrastructure.respositories.transaction_repository import SQLAlchemyTransactionRepository


@pytest.fixture
def account(account_repository):
    account = Account(name="Jenny", balance=Decimal("100.00"))
    account_repository.add(account)
    account_repository.commit()
    return account


@pytest.fixture
def account_repository(async_session):
    return SQLAlchemyAccountRepository(session=async_session)


@pytest.fixture
def transaction_repository(async_session):
    return SQLAlchemyTransactionRepository(session=async_session)