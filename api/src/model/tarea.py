from sqlalchemy import Column, Integer, String, Date
from model import Base
from enum import Enum as PyEnum

class estado(str, PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"

class Tarea(Base):
    __tablename__ = "Tarea"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Enum(estado), nullable=False)
    created_at = Column(Date, index=True)
    updated_at = Column(Date, index=True)
    