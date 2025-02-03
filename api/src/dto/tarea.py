from pydantic import BaseModel, Field
from datetime import datetime
from src.utils.utils import estadoTarea
from pydantic import ConfigDict

class Tarea(BaseModel):
    title: str
    description: str
    status: estadoTarea
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Configuración del modelo para Pydantic v2
    model_config = ConfigDict(use_enum_values=True)  # Esto reemplaza la clase Config
