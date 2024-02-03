from logging.config import dictConfig

from app.infrastructure.app import init_app
from app.infrastructure.config import settings
from app.infrastructure.logging_config import LogConfig


log_config = LogConfig().model_dump()
dictConfig(log_config)

app = init_app()

database_url = settings.database_url

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_config=log_config,
    )
