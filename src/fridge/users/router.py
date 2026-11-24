from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.core.security import hash_password
from fridge.db.session import get_db
from fridge.users.models import User
from fridge.users.schemas import UsersGet, UserCreate, UserRead

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


@router.post("/create_user", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreate,
        session: Annotated[AsyncSession, Depends(get_db)],
):
    """Создание пользователя"""
    # хэшируем пароль
    hashed_password = hash_password(user_data.password)

    # создание пользователя
    user = User(email=user_data.email, hashed_password=hashed_password)

    # добавление объекта в сессию, сохранение изменений и обновление объекта
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
