from pydantic import BaseModel, Field
from bson import ObjectId
from utils.db_connections import PyObjectId
from typing import Optional

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    password: str
    role: str
    
    class Config:
        allow_population_by_field_name = True       # Permite el uso de id en vez de _id en el codigo de la api
        arbitrary_types_allowed = True              # Permite que el modelo acepte tipos personalizados como ObjectId
        json_encoders = {ObjectId: str}             # Define como serializar tipos de datos personalizados al convertirlos a JSON
    