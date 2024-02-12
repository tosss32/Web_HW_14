"""
Модуль для роботи з аватаром користувача.

Містить роут для обробки аватарів користувачів.
"""
from fastapi import APIRouter, Depends, File, UploadFile
from services.users import UserService
from services.cloudinary_service import upload_image

router = APIRouter()

@router.post("/avatar/{user_id}")
async def update_avatar(user_id: int, file: UploadFile = File(...), user_service: UserService = Depends()):
    avatar_public_id = upload_image(file.file)
    user = user_service.update_avatar(user_id, avatar_public_id)
    
    return user