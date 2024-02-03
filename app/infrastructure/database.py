import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.infrastructure.config import settings


Base = declarative_base()

logger = logging.getLogger(__name__)

async_engine = create_async_engine(
    settings.database_url.unicode_string(),
    echo=True,
    future=True,
    pool_pre_ping=True,
    pool_size=8,
    max_overflow=16,
)

async_session = async_sessionmaker(
    async_engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        logger.info(f"DB Pool: {async_engine.pool.status()}")
        yield session
