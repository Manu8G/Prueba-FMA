from src.repository.tareas_repository import TareasRepository
from src.dto.tarea import Tarea
from src.utils.db_connections import mock_db
import pytest
import os
import logging
import asyncio
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


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


# Instanciamos tareas para probar sus funciones
@pytest.fixture(scope="function")   # Crea nuevas instancias de la BD para cada test
def tareas_repo(mock_db):
    repo = TareasRepository()
    repo.db = mock_db  # Sobrescribimos la base de datos con la simulada
    return repo


# Test para crear tarea
@pytest.mark.asyncio
async def test_crear_tarea(tareas_repo):
    tarea = Tarea(title="TEST-Crear Tarea Test", description="TEST-Descripción de la tarea", status="pending", user_id="1")
    resultado = await tareas_repo.crear_tarea(tarea)
    
    assert "inserted_id" in resultado
    assert isinstance(resultado["inserted_id"], str)


# Test para leer tarea concreta, podriamos hacer el test de leer tareas de un usuarios concreto, o 
# del user admin para ello simplemente tenemos que crear mas ejemplos de tareas y llamar a la funcion 
# de listar_tareas
@pytest.mark.asyncio
async def test_leer_tarea(tareas_repo):
    # Insertamos una tarea de prueba en la base de datos simulada
    print("TT TLT POINT1")
    tarea = Tarea(title="TEST-Leer Tarea Test", description="TEST-Descripción de la tarea", status="pending", user_id="1")
    print("TT TLT POINT2")
    taera_insertada = await tareas_repo.crear_tarea(tarea)
    print("TT TLT POINT3")
    tarea_id = taera_insertada["inserted_id"]
    print("TT TLT tarea_id = "+tarea_id)
    
    resultado = await tareas_repo.leer_tarea(str(tarea_id))
    
    assert resultado["_id"] == str(tarea_id)
    assert resultado["title"] == "TEST-Leer Tarea Test"


# Test para actualizar tarea concreta
@pytest.mark.asyncio
async def test_actualizar_tarea(tareas_repo):
    # Insertamos una tarea de prueba
    tarea = Tarea(title="TEST-Tarea Actualizar Test", description="TEST-Descripción Test", status="pending", user_id="12345")
    taera_insertada = await tareas_repo.crear_tarea(tarea)
    tarea_id = taera_insertada["inserted_id"]

    # Creamos un objeto de actualización
    tarea_modificada = Tarea(title="TEST-Tarea Actualizada", description="TEST-Descripción Test", status="pending", user_id="12345")

    resultado = await tareas_repo.actualizar_tarea(str(tarea_id), tarea_modificada)
    
    assert resultado["_id"] == str(tarea_id)
    assert resultado["title"] == "TEST-Tarea Actualizada"  # Se ha actualizado correctamente


# Test para eliminar tarea
@pytest.mark.asyncio
async def test_eliminar_tarea(tareas_repo):
    # Insertamos una tarea
    # Insertamos una tarea de prueba
    tarea = Tarea(title="TEST-Tarea Eliminar Test", description="Descripción Test", status="pending", user_id="12345")
    taera_insertada = await tareas_repo.crear_tarea(tarea)
    tarea_id = taera_insertada["inserted_id"]
    
    resultado = await tareas_repo.eliminar_tarea(str(tarea_id))

    assert resultado == {"message": "Tarea eliminada correctamente"}
    assert await tareas_repo.leer_tarea(str(tarea_id)) == {"message": "Tarea no encontrada, algo ha ido muy mal"}  # Verificar que se eliminó 
