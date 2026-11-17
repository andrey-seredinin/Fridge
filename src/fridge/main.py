from contextlib import asynccontextmanager

from fastapi import FastAPI
from fridge.core.config import settings
from fridge.db.session import engine


# закрытие ресурсов пула соединений
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        # закрыть подключения к БД при остановке приложения
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "project": settings.PROJECT_NAME}

    # Здесь позже будут подключаться роутеры:
    # app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

    return app


app = create_app()
