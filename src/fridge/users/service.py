from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.core.security import hash_password
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

    # Обработка ошибок
    except IntegrityError as exc:
        # Возврат сессии в рабочее состояние
        await session.rollback()

        # Проверка, что почта не занята
        constraint_name = getattr(exc.orig.__cause__, "constraint_name", None)
        if constraint_name == "uq_users_email":
            raise EmailAlreadyExistsError() from exc

        # Остальные ошибки
        raise

    # обновление объекта
    await session.refresh(user)

    return user
