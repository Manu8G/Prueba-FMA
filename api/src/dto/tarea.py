from pydantic import BaseModel
from datetime import datetime
from utils.utils import estadoTarea

class Tarea(BaseModel):
    title: str
    description: str
    status: estadoTarea
    created_at: datetime
    updated_at: datetime
    
    class Config:
        use_enum_values = True  # Convierte Enum automáticamente a su valor
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # Convierte datetime a ISO 8601
        }
    
