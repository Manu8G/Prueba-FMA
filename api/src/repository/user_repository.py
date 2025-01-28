from src.model.user import User

from src.utils.db_connections import db

class UserRepository:
    
    def __init__(self):
        None

    def get_user(self, name: str):
        filtro = {
                "Name": name
            }
        return db.usuarios.find(filtro)
    
    
    def get_role(self, name: str):
        filtro = {
                "Name": name
            }
        return db.usuarios.find(filtro).Role
      
    