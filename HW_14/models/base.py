from dependencies.database import Base
from sqlalchemy import Column, Integer

class BaseModel(Base):
    """
    Базова модель.

    Атрибути:
    - id: Ідентифікаційний номер.
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
