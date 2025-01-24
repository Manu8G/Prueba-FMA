from repository.user_repository import UserRepository
from dto.user import User

class UserService:
  def __init__(self):
    self.user_repository = UserRepository()

  # Las funciones necesarias son las mismas que las descritas en User_repository
  def get_user(self, name: str) -> User:
    try:
      return self.user_repository.get_user_db(name = name)
    except Exception as e:
      raise RuntimeError(f"Something goes wrong {str(e)}")
    

  def obtener_rol(self, name: str):
    try:
      return self.user_repository.obtener_rol(name=name)
    except Exception as e:
      raise RuntimeError(f"AdminService: something goes wrong: {str(e)}")
    

  def list_users_for_admin(self):
    try:
      return self.user_repository.list_users_for_admin()
    except Exception as e:
      raise RuntimeError(f"AdminService: something goes wrong: {str(e)}")
    

  def get_user_id(self, nombre_y_apellidos: str, password: str, role: str):
    try:
      return self.user_repository.get_user_id(nombre_y_apellidos=nombre_y_apellidos, password=password, role=role)
    except Exception as e:
      raise RuntimeError(f"AdminService: something goes wrong: {str(e)}")
