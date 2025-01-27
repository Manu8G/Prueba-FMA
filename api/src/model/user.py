from pydantic import BaseModel, Field
from bson import ObjectId
from utils.db_connections import PyObjectId
from typing import Optional

class User(BaseModel):
    _id: Optional[PyObjectId]
    Name: str
    Password: str
    Role: str
    
    class Config:
        arbitrary_types_allowed = True              # Permite que el modelo acepte tipos personalizados como ObjectId
        json_encoders = {ObjectId: str}             # Define como serializar tipos de datos personalizados al convertirlos a JSON
    