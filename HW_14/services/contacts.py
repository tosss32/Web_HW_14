from repo.contacts import ContactRepo
from schemas.contact import Contact, ContactCreate, ContactUpdate


class ContactService():
    """
    Сервіс для роботи з контактами.

    Атрибути:
    - db: Екземпляр сесії бази даних.
    """
    def __init__(self, db) -> None:
        self.repo = ContactRepo(db=db)

    def get_all_contacts(self) -> list[Contact]:
        """
        Отримати всі контакти.

        Повертає:
        Список всіх контактів.
        """
        all_contacts_from_db = self.repo.get_all()
        result = [Contact.from_orm(item) for item in all_contacts_from_db]
        return result
    
    def create_new(self, create_item: ContactCreate) -> Contact:
        """
        Створити новий контакт.

        Повертає:
        Створений контакт.
        """
        new_item_from_db = self.repo.create(create_item)
        return Contact.from_orm(new_item_from_db)
    
    def get_by_id(self, id: int) -> Contact:
        """
        Отримати контакт за ID.

        Повертає:
        Контакт.
        """
        contact_item = self.repo.get_by_id(id)
        return Contact.from_orm(contact_item)
    
    def update_contact(self, id: int, contact_update: ContactUpdate) -> Contact:
        """
        Оновлення контакту.

        Повертає:
        Оновлений контакт.
        """
        update_item = self.repo.update_by_id(id, contact_update)
        return Contact.from_orm(update_item)
    
    def delete_contact(self, contact_id):
        """
        Видалення контакту.

        """
        return self.repo.delete_by_id(contact_id)
    
    def search_contacts(self, query: str) -> list[Contact]:
        """
        Пошук контакту.

        Повертає:
        Контакт, який відповідає запиту.
        """
        return self.repo.search_contacts(query)
    
    def upcoming_birthdays(self) -> list[Contact]:
        """
        Найближчі дні народження.

        Повертає:
        Список днів народження.
        """
        return self.repo.get_upcoming_birthdays()
