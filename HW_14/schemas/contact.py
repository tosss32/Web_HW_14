from datetime import datetime
from pydantic import BaseModel

class Contact(BaseModel):
    """
    Базова схема контактів

    Атрибути:
    - id: Ідентифікатор в БД
    - first_name: Ім'я контакту.
    - last_name: Прізвище контакту.
    - email: Email контакту.
    - phone_number: Номер телефону контакту.
    - birthday: День народження контакту.
    - additional_data: Додаткові дані про контакт.
    """
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: datetime
    additional_data: str = None
    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    """
    Схема для створення контактів

    Атрибути:
    - first_name: Ім'я контакту.
    - last_name: Прізвище контакту.
    - email: Email контакту.
    - phone_number: Номер телефону контакту.
    - birthday: День народження контакту.
    - additional_data: Додаткові дані про контакт.
    """
    first_name: str
    last_name: str | None
    email: str | None
    phone_number: str
    birthday: datetime | None
    additional_data: str | None


class ContactUpdate(BaseModel):
    """
    Схема для оновлення контактів

    Атрибути:
    - first_name: Ім'я контакту.
    - last_name: Прізвище контакту.
    - email: Email контакту.
    - phone_number: Номер телефону контакту.
    - birthday: День народження контакту.
    - additional_data: Додаткові дані про контакт.
    """
    first_name: str | None
    last_name: str | None
    email: str | None
    phone_number: str | None
    birthday: datetime | None
    additional_data: str | None