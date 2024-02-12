"""
Модуль для з'єднання з базою даних.

Містить функції для створення сесій бази даних та встановлення з'єднання з базою даних.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://postgres:pass@localhost/hw11"  
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
       