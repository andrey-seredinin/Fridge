from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.core.security import hash_password
from fridge.db.session import get_db
from fridge.users.exceptions import EmailAlreadyExistsError
from fridge.users.models import User
from fridge.users.schemas import UserCreate


async def create_user_service(
        user_data: UserCreate,
        session: AsyncSession,
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
    except IntegrityError as exc:
        # Возврат сессии в рабочее состояние
        await session.rollback()
        raise EmailAlreadyExistsError() from exc

    # обновление объекта
    await session.refresh(user)

    return user
