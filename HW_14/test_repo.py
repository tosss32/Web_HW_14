import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from schemas.contact import ContactUpdate
from repo.contacts import ContactRepo
from models.contact import ContactDB
from repo.user import UserRepo
from models.users import UsertDB


class TestContactRepo(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.repo = ContactRepo(db=self.session)

    def test_get_all(self):
        expected_result = [ContactDB(id=1, first_name = "Flo",
                                last_name = "Wer",
                                email = "flower@ukr.net",
                                phone_number = "025123654789",
                                birthday = "12-02-2000",
                                additional_data = "__" ), 
                ContactDB(id=2, first_name = "Teddy",
                                last_name = "Bear",
                                email = "teddy@bear.net",
                                phone_number = "098321654987",
                                birthday = "03-03-2003",
                                additional_data = "__" )]
        self.session.query.return_value.all.return_value = expected_result
        result = self.repo.get_all()
        self.assertEqual(result, expected_result)

    
    def test_get_by_id(self):
        expected_id = 1
        expected_contact = ContactDB(id=1, first_name = "Flo",
                                last_name = "Wer",
                                email = "flower@ukr.net",
                                phone_number = "025123654789",
                                birthday = "12-02-2000",
                                additional_data = "__" )
        self.session.query.return_value.filter.return_value.first.return_value = expected_contact
        result = self.repo.get_by_id(expected_id)
        self.assertEqual(result, expected_contact)

    def test_update_by_id(self):
        contact_id = 1
        contact_update = ContactUpdate(first_name="Po")
        db_contact = ContactDB(id=1, first_name = "Flo",
                                last_name = "Wer",
                                email = "flower@ukr.net",
                                phone_number = "025123654789",
                                birthday = "12-02-2000",
                                additional_data = "__" )
        self.session.query.return_value.filter.return_value.first.return_value = db_contact
        result = self.repo.update_by_id(contact_id, contact_update)
        self.assertEqual(result.first_name, "Po")

    def test_delete_by_id(self):
        contact_id = 1
        db_contact = ContactDB(id=1, first_name = "Flo",
                                last_name = "Wer",
                                email = "flower@ukr.net",
                                phone_number = "025123654789",
                                birthday = "12-02-2000",
                                additional_data = "__" )
        self.session.query.return_value.filter.return_value.first.return_value = db_contact
        result = self.repo.delete_by_id(contact_id)
        self.session.delete.assert_called_once_with(db_contact)
        self.session.commit.assert_called_once()
        self.assertEqual(result, db_contact)

    def test_search_contacts(self):
        query = "Teddy"
        expected_result = [ContactDB(id=2, first_name = "Teddy",
                                last_name = "Bear",
                                email = "teddy@bear.net",
                                phone_number = "098321654987",
                                birthday = "03-03-2003",
                                additional_data = "__" )]
        self.session.query.return_value.filter.return_value.all.return_value = expected_result
        result = self.repo.search_contacts(query)
        self.assertEqual(result, expected_result)

    def test_get_upcoming_birthdays(self):
        today = datetime.now().date()
        end_date = today + timedelta(days=7)
        expected_result = [ContactDB(id=1, first_name = "Flo",
                                last_name = "Wer",
                                email = "flower@ukr.net",
                                phone_number = "025123654789",
                                birthday = "12-02-2000",
                                additional_data = "__" )]
        self.session.query.return_value.filter.return_value.all.return_value = expected_result
        result = self.repo.get_upcoming_birthdays()
        self.assertEqual(result, expected_result)

class TestUserRepo(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock()
        self.repo = UserRepo(db=self.session)

    """  
    def test_create(self):
        user_instance = UsertDB(username="test_user", password="test_password")
        result = self.repo.create(user_instance)
        self.session.add.assert_called_once_with(user_instance)
        self.session.commit.assert_called_once() 
    """

    def test_get_by_username(self):
        username = "test_user"
        self.repo.get_by_username(username)
        self.session.query.return_value.filter.return_value.first.return_value(UsertDB.username == username)

    def test_get_by_email(self):
        email = "test@example.com"
        self.repo.get_by_email(email)
        self.session.query.return_value.filter.return_value.first.return_value(UsertDB.email == email)

    def test_get_user_check_pass_correct_password(self):
        username = "test_user"
        password = "test_password"
        user_instance = UsertDB(username=username)
        user_instance.password, user_instance.salt = self.repo.hash_password(password)
        self.session.query.return_value.filter.return_value.first.return_value = user_instance
        result = self.repo.get_user_check_pass(username, password)
        self.assertEqual(result, user_instance)

    def test_get_user_check_pass_incorrect_password(self):
        username = "test_user"
        password = "incorrect_password"
        user_instance = UsertDB(username=username)
        user_instance.password, user_instance.salt = self.repo.hash_password("test_password")
        self.session.query.return_value.filter.return_value.first.return_value = user_instance
        result = self.repo.get_user_check_pass(username, password)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()