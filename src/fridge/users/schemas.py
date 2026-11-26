import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UsersGetOrRead(BaseModel):
    """Схема для получения всех пользователей"""
    id: uuid.UUID
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    # pydantic читает данные непосредственно из объекта SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Схема для создания пользователя"""
    email: str
    password: str
