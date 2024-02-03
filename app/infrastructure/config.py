from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    database_url: PostgresDsn = MultiHostUrl(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )
    host: str = "localhost"
    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
