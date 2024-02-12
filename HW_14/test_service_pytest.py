import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from schemas.contact import Contact, ContactCreate, ContactUpdate
from repo.contacts import ContactRepo
from services.contacts import ContactService


@pytest.fixture
def mock_contact_repo():
    return MagicMock(spec=ContactRepo)


@pytest.fixture
def contact_service(mock_contact_repo):
    return ContactService(db=mock_contact_repo)


def test_get_all_contacts(contact_service, mock_contact_repo):
    mock_contacts = [
        Contact(id=1, name="John Doe", email="john@example.com"),
        Contact(id=2, name="Jane Smith", email="jane@example.com"),
    ]
    mock_contact_repo.get_all.return_value = mock_contacts

    result = contact_service.get_all_contacts()

    assert result == mock_contacts


def test_create_new_contact(contact_service, mock_contact_repo):
    new_contact_data = ContactCreate(name="Alice", email="alice@example.com")
    mock_new_contact = Contact(id=1, name="Alice", email="alice@example.com")
    mock_contact_repo.create.return_value = mock_new_contact

    result = contact_service.create_new(new_contact_data)

    assert result == mock_new_contact


def test_get_contact_by_id(contact_service, mock_contact_repo):
    contact_id = 1
    mock_contact = Contact(id=1, name="John Doe", email="john@example.com")
    mock_contact_repo.get_by_id.return_value = mock_contact

    result = contact_service.get_by_id(contact_id)

    assert result == mock_contact


def test_update_contact(contact_service, mock_contact_repo):
    contact_id = 1
    update_data = ContactUpdate(name="Jane Doe")
    mock_updated_contact = Contact(id=1, name="Jane Doe", email="john@example.com")
    mock_contact_repo.update_by_id.return_value = mock_updated_contact

    result = contact_service.update_contact(contact_id, update_data)

    assert result == mock_updated_contact


def test_delete_contact(contact_service, mock_contact_repo):
    contact_id = 1

    result = contact_service.delete_contact(contact_id)

    mock_contact_repo.delete_by_id.assert_called_once_with(contact_id)


def test_search_contacts(contact_service, mock_contact_repo):
    query = "Doe"
    mock_matching_contacts = [
        Contact(id=1, name="John Doe", email="john@example.com"),
        Contact(id=2, name="Jane Doe", email="jane@example.com"),
    ]
    mock_contact_repo.search_contacts.return_value = mock_matching_contacts

    result = contact_service.search_contacts(query)

    assert result == mock_matching_contacts


def test_upcoming_birthdays(contact_service, mock_contact_repo):
    mock_upcoming_birthdays = [
        Contact(id=1, name="John Doe", email="john@example.com"),
        Contact(id=2, name="Jane Smith", email="jane@example.com"),
    ]
    mock_contact_repo.get_upcoming_birthdays.return_value = mock_upcoming_birthdays

    result = contact_service.upcoming_birthdays()

    assert result == mock_upcoming_birthdays
