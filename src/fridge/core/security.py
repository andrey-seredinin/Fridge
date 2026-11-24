from pwdlib import PasswordHash


# экземпляр пароля для хеширования
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Хэширует пароль."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля сохранённому хэшу."""
    return password_hash.verify(plain_password, hashed_password)
