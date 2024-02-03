from functools import partial

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.domain.accounts.account_repository import IAccountRepository
from app.domain.accounts.exceptions import AccountDoesNotExist
from app.infrastructure.database import get_session
from app.infrastructure.respositories.account_repository import SQLAlchemyAccountRepository
from app.presentation.endpoints.accounts import router as accounts_routes


def handle_exceptions(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    @app.exception_handler(AccountDoesNotExist)
    async def account_does_not_exist_exception_handler(
        request: Request, exc: AccountDoesNotExist
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder({"detail": str(exc)}),
        )


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

    handle_exceptions(app)

    return app
