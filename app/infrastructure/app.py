from functools import partial

from fastapi import FastAPI

from app.domain.accounts.account_repository import IAccountRepository
from app.infrastructure.database import get_session
from app.infrastructure.respositories.account_repository import SQLAlchemyAccountRepository
from app.presentation.endpoints.accounts import router as accounts_routes


def init_app():
    app = FastAPI(
        title="Bank API",
        description="Bank API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    app.include_router(accounts_routes, prefix="/accounts")

    app.dependency_overrides[get_session] = get_session
    app.dependency_overrides[IAccountRepository] = partial(SQLAlchemyAccountRepository)

    return app
