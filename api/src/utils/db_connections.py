from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

from utils.config import Config

config = Config()

######################################### Conexion mongo
import motor.motor_asyncio
from core.config import settings


client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client.UltimateBot

##################################################


def create_db_connection():
    engine = create_engine(config.get("MYSQL.URL"), echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

def init_db():
    engine = create_engine(config.get("MSQL.URL"), echo=True)
    Base.metadata.create_all(engine)
    
    session = create_db_connection(engine)
    