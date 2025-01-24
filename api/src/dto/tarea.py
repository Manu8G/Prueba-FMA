from pydantic import BaseModel
from datetime import date
from enum import Enum

class estado(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
    

class Tarea(BaseModel):
    id: str
    title: str
    description: str
    status: estado
    created_at: date
    updated_at: date
    
