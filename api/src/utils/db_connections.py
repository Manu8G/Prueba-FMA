from motor.motor_asyncio import AsyncIOMotorClient
from src.utils.config import Config
from bson import ObjectId
import os
#import mongomock_motor
import pytest

config = Config()

if "PYTEST_CURRENT_TEST" not in os.environ:
    client = AsyncIOMotorClient(config.get("MONGODB.URL"))
    db = client["pruebaTecnica"]
else:
    # client = mongomock_motor.AsyncMongoMockClient()
    client = AsyncIOMotorClient(config.get("MONGODB.URL"))
    db = client["test_database"]
    
# Creamos una DB de prueba para tratar sobre datos no sensibles y probar el funcionamiento correcto de las funciones
@pytest.fixture(scope="function")
async def mock_db():
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

# Convertidor para ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
