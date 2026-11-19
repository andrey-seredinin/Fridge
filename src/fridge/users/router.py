from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.db.session import get_db
from fridge.users.models import User
from fridge.users.schemas import UsersGet


router = APIRouter(
    # общий префикс URL для всех эндпоинтов этого роутера
    prefix="/users",
    # группировка эндпоинтов в Swagger документации
    tags=["Users"],
)


@router.get("/", response_model=list[UsersGet])
async def get_users(
    session: Annotated[AsyncSession, Depends(get_db)],
):
    """Получение всех пользователей"""
    # запрос к БД
    result = await session.execute(select(User))

    # излечение из запроса к БД информации
    users = result.scalars().all()

    return users
