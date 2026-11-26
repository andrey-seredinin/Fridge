from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.db.session import get_db
from fridge.users.models import User
from fridge.users.schemas import UserCreate


async def get_user_by_email(
        session: AsyncSession,
        email: str
) -> User | None:
    """ Функция проверки пользователя в БД по email"""
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    return user
