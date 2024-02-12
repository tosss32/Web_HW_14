from sqlalchemy import  Column, String, DateTime
from .base import BaseModel

class UsertDB(BaseModel):
    """
    Модель користувача.

    Атрибути:
    - username: Логін користувача.
    - email: Email користувача для аутентифікації.
    - password: Пароль користувача.
    - salt: Сіль до паролю користувача.
    - avatar_public_id: ID аватару користовача.
    """
    __tablename__ = "users"
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    salt = Column(String)
    avatar_public_id = Column(String, default=None)

    