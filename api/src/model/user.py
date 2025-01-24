from sqlalchemy import Column, Integer, String, Boolean
from model import Base

class User(Base):
    __tablename__ = "Usuario"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_y_apellidos = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    rol = Column(String, index=True)