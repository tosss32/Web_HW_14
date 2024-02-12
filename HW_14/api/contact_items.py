"""
Модуль для визначення API для контактів.

Містить роути та функції для обробки HTTP-запитів, що стосуються контактів.
"""
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from schemas.contact import Contact, ContactCreate, ContactUpdate
from dependencies.database import get_db, SessionLocal
from services.contacts import ContactService
from starlette.responses import JSONResponse
from fastapi_ratelimiter import RateLimited, RedisDependencyMarker
from fastapi_ratelimiter.strategies import BucketingRateLimitStrategy
import aioredis


router = APIRouter()
app = FastAPI()
app.dependency_overrides[RedisDependencyMarker] = aioredis.from_url("redis://localhost")


@router.get("/")
async def list_contacts(db: SessionLocal = Depends(get_db)) -> list[Contact]:
    contact_items = ContactService(db=db).get_all_contacts()
    return contact_items


@router.get("/{id}")
async def get_detail(id: int, db: SessionLocal = Depends(get_db)) -> Contact:
    contact_item = ContactService(db=db).get_by_id(id)
    return contact_item


@router.post("/", response_class=JSONResponse,
    dependencies=[
        Depends(RateLimited(BucketingRateLimitStrategy(rate="10/60s")))
    ])
async def create_contact(contact_item: ContactCreate, db: SessionLocal = Depends(get_db)) -> Contact:
    new_item = ContactService(db=db).create_new(contact_item)
    return new_item

@router.put("/{id}")
async def update_contact(id: int, contact_update: ContactUpdate, db: SessionLocal = Depends(get_db)):
    updated_contact = ContactService(db=db).update_contact(id, contact_update)
    return updated_contact

@router.delete("/{id}")
async def delete_contact(id: int, db: SessionLocal = Depends(get_db)):
    contact_service = ContactService(db=db)
    deleted_contact = contact_service.delete_contact(id)
    if not deleted_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}


@router.get("/search/")
async def search_contacts(query: str, db: SessionLocal = Depends(get_db)) -> list[Contact]:
    contact_service = ContactService(db=db)
    contacts = contact_service.search_contacts(query)
    return contacts

@router.get("/upcoming_birthdays/")
async def upcoming_birthdays(db: SessionLocal = Depends(get_db)) -> list[Contact]:
    contact_service = ContactService(db=db)
    contacts = contact_service.upcoming_birthdays()
    return contacts
