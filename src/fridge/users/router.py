from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.db.session import get_db
from fridge.users.exceptions import EmailAlreadyExistsError
from fridge.users.models import User
from fridge.users.schemas import UsersGetOrRead, UserCreate
from fridge.users.service import create_user_service

router = APIRouter(
    # общий префикс URL для всех эндпоинтов этого роутера
    prefix="/users",
    # группировка эндпоинтов в Swagger документации
    tags=["Users"],
)


@router.get("/", response_model=list[UsersGetOrRead])
async def get_users(
    session: Annotated[AsyncSession, Depends(get_db)],
):
    """Получение всех пользователей"""
    # запрос к БД
    result = await session.execute(select(User))

    # излечение из запроса к БД информации
    users = result.scalars().all()

    return users


@router.post("/create_user", response_model=UsersGetOrRead, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreate,
        session: Annotated[AsyncSession, Depends(get_db)],
):
    """Создание пользователя"""
    try:
        # функция создания пользователя в сервисном слое
        return await create_user_service(user_data, session)

    # Обработка ошибки создания пользователя с одинаковой почтой
    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с такой почтой уже существует'
        )
