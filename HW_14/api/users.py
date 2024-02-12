"""
Модуль для визначення API для користувачів.

Містить роути та функції для обробки HTTP-запитів, що стосуються користувачів.
"""
from fastapi import APIRouter, Depends, HTTPException
from dependencies.database import get_db, SessionLocal
from schemas.user import User, UserVerification
from dependencies.auth import create_access_token, get_current_user, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from services.users import UserService



app = APIRouter()

@app.post("/register/", response_model=User)
async def register(user: User, db: SessionLocal = Depends(get_db)):
    user_service = UserService(db)
    
    return user_service.create_new(user)

@app.post("/token/", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_for_auth(form_data.username, form_data.password)
    access_token = create_access_token(username = user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected-resource/", response_model=User)
async def protected_resource(current_user: User = Depends(get_current_user)):
    return current_user

def authenticate_user(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

@app.post("/verify-email/")
async def verify_email(user_verification: UserVerification, db: SessionLocal = Depends(get_db)):
    user_service = UserService(db)
    user_service.verify_user_email(user_verification)
    return {"message": "Email successfully verified"}

