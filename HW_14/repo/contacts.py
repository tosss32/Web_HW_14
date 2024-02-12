from sqlalchemy.orm import Session
from models.contact import ContactDB
from schemas.contact import ContactUpdate
from datetime import datetime, timedelta
from sqlalchemy.sql import extract


class ContactRepo():
    """
    Модуль для роботи з репозиторієм контактів.

    Атрибути:
    - db: Екземпляр сесії бази даних.
    """
    def __init__(self, db) -> None:
        self.db = db

    def get_all(self) -> list[ContactDB]:
        """
        Отримати всі контакти.

        Повертає:
        Всі контакти з БД.

        """
        return self.db.query(ContactDB).all()
    
    def create(self, contact_item):
        """
        Створити новий контакт.

        Повертає:
        Новий контакт.

        """
        new_item = ContactDB(**contact_item.dict())
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item
    

    def get_by_id(self, id):
        """
        Отримати контакт по id.

        Повертає:
        Контакт по id.

        """
        return self.db.query(ContactDB).filter(ContactDB.id == id).first()
    
        
    def update_by_id(self, id: int, contact_update: ContactUpdate):
        """
        Оновити контакт по id.

        Повертає:
        Оновлений контакт по id.

        """
        db_contact = self.db.query(ContactDB).filter(ContactDB.id == id).first()
        if db_contact:
            if "email" in contact_update.dict(exclude_unset=True):
                new_email = contact_update.email
                existing_contact = self.db.query(ContactDB).filter(ContactDB.email == new_email, ContactDB.id != id).first()
                if existing_contact:
                    raise ValueError("Email already exists for another contact")
            for key, value in contact_update.dict(exclude_unset=True).items():
                setattr(db_contact, key, value)
            try:
                self.db.commit()
                self.db.refresh(db_contact)
            except IntegrityError as e:
                self.db.rollback()
                raise ValueError("Email already exists for another contact") from e
        return db_contact
    
    def delete_by_id(self, contact_id):
        """
        Видалити контакт по id.

        Повертає:
        Контакт по id.

        """
        db_contact = self.db.query(ContactDB).filter(ContactDB.id == contact_id).first()
        if db_contact:
            self.db.delete(db_contact)
            self.db.commit()
        return db_contact
    

    def search_contacts(self, query: str) -> list[ContactDB]:
        """
        Пошук контакту.

        Повертає:
        Контакт за запитом.

        """
        return (
            self.db.query(ContactDB)
            .filter(
                (ContactDB.first_name.ilike(f"%{query}%"))
                | (ContactDB.last_name.ilike(f"%{query}%"))
                | (ContactDB.email.ilike(f"%{query}%"))
            )
            .all()
        )
    

    def get_upcoming_birthdays(self) -> list[ContactDB]:
        """
        Майбутні дні народження.

        Повертає:
        Список днів народження на наступному тижні.

        """
        today = datetime.now().date()
        end_date = today + timedelta(days=7)
        birthday_month = extract('month', ContactDB.birthday)
        birthday_day = extract('day', ContactDB.birthday)

        return (
            self.db.query(ContactDB)
            .filter(
                (
                    (birthday_month == today.month)
                    & (birthday_day >= today.day)
                    & (birthday_day <= end_date.day)
                )
                | (
                    (birthday_month == (today.month % 12) + 1)
                    & (birthday_day <= end_date.day)
                )
            )
            .all()
        )