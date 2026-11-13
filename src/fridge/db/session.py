from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from fridge.core.config import settings

# Создаём асинхронный движок
engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    # Проверка живости соединения
    pool_pre_ping=True,
    # Логировать SQL в дебаге
    echo=settings.DEBUG,
)

# Фабрика сессий
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    """Зависимость FastAPI для получения сессии БД на один запрос."""
    async with async_session_factory() as session:
        try:
            yield session
            # Коммит лучше делать в сервисном слое, но для простых эндпоинтов можно здесь
            # await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
