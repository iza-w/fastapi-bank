from app.infrastructure.app import init_app
from app.infrastructure.config import settings


app = init_app()

database_url = settings.database_url

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=settings.host, port=settings.port, reload=True
    )
