from pydantic import BaseModel, Field
from bson import ObjectId
from utils.db_connections import PyObjectId
from enum import Enum
from datetime import datetime
from utils.utils import estadoTarea
from typing import Optional

class Tarea(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id") 
    title: str  
    description: Optional[str] = None  
    status: estadoTarea
    created_at: datetime
    updated_at: datetime
    