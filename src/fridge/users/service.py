from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.core.security import hash_password
from fridge.db.session import get_db
from fridge.users.models import User
from fridge.users.schemas import UserCreate


async def create_user_service(
        user_data: UserCreate,
        session: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Создание пользователя в сервисном слое"""
    # хэшируем пароль
    hashed_password = hash_password(user_data.password)

    # создание пользователя
    user = User(email=user_data.email, hashed_password=hashed_password)

    # добавление объекта в сессию
    session.add(user)

    try:
        # сохранение изменений
        await session.commit()

    # Обработка ошибки
    except IntegrityError:
        # Возврат сессии в рабочее состояние
        await session.rollback()
        raise

    # обновление объекта
    await session.refresh(user)

    return user
