from src.model.user import User
from bson import ObjectId
from src.utils.db_connections import db

class UserRepository:
    
    def __init__(self):
        None

    async def get_user(self, id: str):
        filtro = {
                "_id": id
            }
        coleccion = db["usuarios"]
        return await coleccion.find(filtro)
    
    
    async def get_role(self, id: str):
        filtro = {
            "_id": ObjectId(id)
        }
        coleccion = db["usuarios"]
        usuario = await coleccion.find_one(filtro)
        rol = usuario["Role"]
        # print("ARCHIVO 3"+ str(rol))
        return rol 
    
    
    async def get_user_info(self, id: str):
        filtro = {
            "_id": ObjectId(id)
        }
        coleccion = db["usuarios"]
        print("IDIDIDID: "+id)
        print("COLECCION: "+str(coleccion))
        usuario = await coleccion.find_one(filtro)
        print("ARCHIVO D"+str(usuario))
        return usuario
      
    