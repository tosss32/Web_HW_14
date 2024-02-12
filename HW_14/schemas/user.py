from pydantic import BaseModel


class User(BaseModel):
    """
    Базова схема користувачів

    Атрибути:
    - username: Логін користувача
    - email: Email користувача.
    - password: Пароль користувача.
    - is_verified: Чи верифікований користувач.
    - avatar_public_id: ID аватару.
    """
    username: str
    email: str
    password: str
    is_verified: bool = False
    avatar_public_id: str = None

    class Config:
        from_attributes = True

class UserVerification(BaseModel):
    token: str

class UserUpdate(BaseModel):
    avatar_url: str
