from motor.motor_asyncio import AsyncIOMotorClient
from model import Base
from utils.config import Config
from bson import ObjectId

config = Config()

client = AsyncIOMotorClient(config.get("MONGO.URL"))
db = client["pruebaTecnica"]
    
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
