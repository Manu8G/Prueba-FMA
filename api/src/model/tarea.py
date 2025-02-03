from pydantic import BaseModel
from utils.db_connections import PyObjectId
from datetime import datetime
from utils.utils import estadoTarea
from typing import Optional

class Tarea(BaseModel):
    _id: Optional[PyObjectId] # = Field(alias="_id") Se podria haber usado alias 
    title: str  
    description: Optional[str] = None  
    status: estadoTarea
    created_at: datetime
    updated_at: datetime
    user_id: Optional[PyObjectId]