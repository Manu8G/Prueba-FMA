import pytest
import mongomock
from bson import ObjectId
from src.repository.tareas_repository import TareasRepository
from src.dto.tarea import Tarea
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


# Creamos una DB de prueba para tratar sobre datos no sensibles y probar el funcionamiento correcto de las funciones
@pytest.fixture
def mock_db():
    client = mongomock.MongoClient()
    db = client["test_database"]
    db.tareas = db["tareas"] 
    '''
    db.tareas.insert_many(
        [
            {
                "title": "TEST-Crear backend",
                "description": "TEST-Utilizaremos FastApi para la creacion del backend",
                "status": "completed",
                "created_at": new Date(),
                "updated_at": new Date("2025-01-30T12:49:51Z"),
                "user_id": 1
            },{
                "title": "TEST-Configurar AWS",
                "description": "TEST-Utilizaremos un EC2 para ejecutar nuestro docker",
                "status": "in progress",
                "created_at": new Date(),
                "updated_at": new Date("2025-01-31T19:23:17Z"),
                "user_id": 1
            },{
                "title": "TEST-Montar BD de Mongo",
                "description": "TEST-Utilizaremos una BD de Mongo para guardar las colecciones de datos necesarias para la aplicación",
                "status": "in progress",
                "created_at": new Date(),
                "updated_at": new Date("2025-01-31T09:21:56Z"),
                "user_id": 2
            },{
                "title": "TEST-Crear Docker",
                "description": "TEST-Crear un contenedor docker que guarde la BD y el backend de la aplicación",
                "status": "completed",
                "created_at": new Date(),
                "updated_at": new Date("2025-01-30T11:12:13Z"),
                "user_id": 2
            },{
                "title": "TEST-Crear Frontend",
                "description": "TEST-Creación de un frontend simple de Angular para poder visualizar facilmente la aplicación",
                "status": "pending",
                "created_at": new Date(),
                "updated_at": new Date(),
                "user_id": 2
            }
        ]
    )'''
    db.usuarios = db["usuarios"] 
    '''
    db.usuarios.insert_many(
        [
            {
                "user_id": 1,
                "Name": "AdminCarlos",
                "Password": "1234",
                "Role": "admin"
            },{
                "user_id": 2,
                "Name": "userNicolas",
                "Password": "1234",
                "Role": "user"
            }
        ]
    )
    '''
    return db

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
    tarea_id = tareas_repo.db.tareas.insert_one({
        "title": "Tarea Test",
        "description": "Descripción Test",
        "status": "pending",
        "user_id": "12345"
    }).inserted_id

    resultado = await tareas_repo.leer_tarea(str(tarea_id))
    
    assert resultado["_id"] == str(tarea_id)
    assert resultado["title"] == "Tarea Test"


# Test para actualizar tarea concreta
@pytest.mark.asyncio
async def test_actualizar_tarea(tareas_repo):
    # Insertamos una tarea de prueba
    tarea_id = tareas_repo.db.tareas.insert_one({
        "title": "Vieja Tarea",
        "description": "Vieja descripción",
        "status": "pending",
        "user_id": "12345"
    }).inserted_id

    # Creamos un objeto de actualización
    tarea_modificada = Tarea(title="Nueva Tarea")

    resultado = await tareas_repo.actualizar_tarea(str(tarea_id), tarea_modificada)
    
    assert resultado["_id"] == str(tarea_id)
    assert resultado["title"] == "Nueva Tarea"  # Se ha actualizado correctamente


# Test para eliminar tarea
@pytest.mark.asyncio
async def test_eliminar_tarea(tareas_repo):
    # Insertamos una tarea
    tarea_id = tareas_repo.db.tareas.insert_one({
        "title": "Tarea a eliminar",
        "description": "Descripción",
        "status": "pending",
        "user_id": "12345"
    }).inserted_id

    resultado = await tareas_repo.eliminar_tarea(str(tarea_id))

    assert resultado == {"message": "Tarea eliminada correctamente"}
    assert tareas_repo.db.tareas.count_documents({"_id": tarea_id}) == 0  # Verificar que se eliminó
