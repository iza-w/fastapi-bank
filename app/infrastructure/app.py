from fastapi import FastAPI


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

    return app
