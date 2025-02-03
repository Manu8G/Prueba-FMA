from src.repository.tareas_repository import TareasRepository
from src.dto.tarea import Tarea
from src.utils.db_connections import mock_db
import pytest
import os
import logging
from src.controller.tarea import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.config import Config

config=Config()
logging.info(config.get("MONGODB"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(router)

@pytest.fixture(autouse=True)
def set_working_directory():
    # Guarda el directorio de trabajo original
    original_dir = os.getcwd()
    # Cambia el directorio al directorio raíz del proyecto
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    yield
    # Restaura el directorio de trabajo original después de la prueba
    os.chdir(original_dir)


# Instanciamos tareas para probar sus funciones
@pytest.fixture
def tareas_repo(mock_db):
    repo = TareasRepository()
    repo.db = mock_db  # Sobrescribimos la base de datos con la simulada
    return repo


# Test para crear tarea
@pytest.mark.asyncio
async def test_crear_tarea(tareas_repo):
    tarea = Tarea(title="TEST-Nueva Tarea Test", description="TEST-Descripción de la tarea", status="pending", user_id="1")
    resultado = await tareas_repo.crear_tarea(tarea)
    
    assert "inserted_id" in resultado
    assert isinstance(resultado["inserted_id"], str)


# Test para leer tarea concreta, podriamos hacer el test de leer tareas de un usuarios concreto, o 
# del user admin para ello simplemente tenemos que crear mas ejemplos de tareas y llamar a la funcion 
# de listar_tareas
@pytest.mark.asyncio
async def test_leer_tarea(tareas_repo):
    # Insertamos una tarea de prueba en la base de datos simulada
    tarea = await tareas_repo.db.tareas.insert_one({
        "title": "Tarea Test",
        "description": "Descripción Test",
        "status": "pending",
        "user_id": "12345"
    })
    tarea_id = tarea.inserted_id

    resultado = await tareas_repo.leer_tarea(str(tarea_id))
    
    assert resultado["_id"] == str(tarea_id)
    assert resultado["title"] == "Tarea Test"


# Test para actualizar tarea concreta
@pytest.mark.asyncio
async def test_actualizar_tarea(tareas_repo):
    # Insertamos una tarea de prueba
    tarea = await tareas_repo.db.tareas.insert_one({
        "title": "Vieja Tarea",
        "description": "Vieja descripción",
        "status": "pending",
        "user_id": "12345"
    })
    tarea_id = tarea.inserted_id

    # Creamos un objeto de actualización
    tarea_modificada = Tarea(title="Nueva Tarea")

    resultado = await tareas_repo.actualizar_tarea(str(tarea_id), tarea_modificada)
    
    assert resultado["_id"] == str(tarea_id)
    assert resultado["title"] == "Nueva Tarea"  # Se ha actualizado correctamente


# Test para eliminar tarea
@pytest.mark.asyncio
async def test_eliminar_tarea(tareas_repo):
    # Insertamos una tarea
    tarea = await tareas_repo.db.tareas.insert_one({
        "title": "Tarea a eliminar",
        "description": "Descripción",
        "status": "pending",
        "user_id": "12345"
    })
    tarea_id = tarea.inserted_id

    resultado = await tareas_repo.eliminar_tarea(str(tarea_id))

    assert resultado == {"message": "Tarea eliminada correctamente"}
    assert tareas_repo.db.tareas.count_documents({"_id": tarea_id}) == 0  # Verificar que se eliminó
