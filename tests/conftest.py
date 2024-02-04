from functools import partial
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.domain.accounts.account_repository import IAccountRepository
from app.domain.transactions.transaction_repository import ITransactionRepository
from app.infrastructure.database import (
    Base,
    get_session,
)
from app.infrastructure.respositories.account_repository import SQLAlchemyAccountRepository
from app.infrastructure.respositories.transaction_repository import SQLAlchemyTransactionRepository


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)


pytestmark = pytest.mark.asyncio

pytest_plugins = ["tests.fixtures"]


@pytest_asyncio.fixture(scope="function", name="async_session")
async def async_session_fixture() -> AsyncGenerator:
    async_session = async_sessionmaker(
        async_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    async with async_session() as session:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest.fixture(scope="function")
def app(async_session):
    from app.infrastructure.app import init_app

    app = init_app()

    def override_get_session():
        return async_session

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[IAccountRepository] = partial(SQLAlchemyAccountRepository)
    app.dependency_overrides[ITransactionRepository] = partial(
        SQLAlchemyTransactionRepository
    )

    return app


@pytest.fixture(scope="function")
def async_client(app):
    return AsyncClient(app=app, base_url="http://localhost")
