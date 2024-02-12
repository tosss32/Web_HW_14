from sqlalchemy import  Column, String, DateTime
from .base import BaseModel, Base

class ContactDB(BaseModel):
    """
    Модель контакту.

    Атрибути:
    - first_name: Ім'я контакту.
    - last_name: Прізвище контакту.
    - email: Email контакту.
    - phone_number: Номер телефону контакту.
    - birthday: День народження контакту.
    - additional_data: Додаткові дані про контакт.
    """
    __tablename__ = "contacts"
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    birthday = Column(DateTime)
    additional_data = Column(String, nullable=True)