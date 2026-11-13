from fastapi import FastAPI
from fridge.core.config import settings


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "project": settings.PROJECT_NAME}

    # Здесь позже будут подключаться роутеры:
    # app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

    return app


app = create_app()
