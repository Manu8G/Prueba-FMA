from pydantic import BaseModel
from datetime import date
from enum import Enum
from utils.utils import estadoTarea

class Tarea(BaseModel):
    id: str
    title: str
    description: str
    status: estadoTarea
    created_at: date
    updated_at: date
    
