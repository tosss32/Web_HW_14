from fastapi import FastAPI
from api.contact_items import router as contact_router
from api.users import app as user_router
from api.avatar import router as avatar_router
from models import contact
from dependencies.database import engine
from fastapi.middleware.cors import CORSMiddleware

contact.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contact_router, prefix="/contact")
app.include_router(user_router, prefix="/users")
app.include_router(avatar_router, prefix="/avatars", tags=["avatars"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"OK": True}

