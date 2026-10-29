from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ASYNC_DRIVER = "postgresql+asyncpg"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    # Значение по умолчанию нужно, чтобы приложение поднималось там, где секрет не задан:
    # в CI и при прогоне миграций. В продакшене SECRET_KEY приходит из окружения.
    secret_key: str = "insecure-development-key"

    @field_validator("database_url")
    @classmethod
    def with_async_driver(cls, value: str) -> str:
        # Хостинг отдаёт адрес как postgres://…, асинхронному движку нужен свой драйвер.
        scheme, separator, rest = value.partition("://")
        if not separator:
            return value
        if scheme in ("postgres", "postgresql"):
            return f"{ASYNC_DRIVER}://{rest}"
        return value


settings = Settings()
