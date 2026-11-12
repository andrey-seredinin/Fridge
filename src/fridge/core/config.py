from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Приложение
    PROJECT_NAME: str = "My Scalable API fridge"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"

    # База данных
    # URL для асинхронного подключения
    DATABASE_URL: str = Field(
        ...,
        description="Async PostgreSQL DSN, e.g. postgresql+asyncpg://user:pass@host:port/dbname"
    )
    # Постоянно открытые соединения
    DB_POOL_SIZE: int = 5
    # Соединения сверх лимита(временные)
    DB_MAX_OVERFLOW: int = 10

    # Безопасность
    SECRET_KEY: str = Field(..., min_length=32)

    # Настройка
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Создаём единственный экземпляр настроек
settings = Settings()