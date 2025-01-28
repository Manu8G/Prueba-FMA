from src.repository.user_repository import UserRepository
from src.dto.user import User 

class UserService:
  def __init__(self):
    self.user_repository = UserRepository()

  
  def get_user(self, name: str):
    try:
      return self.user_repository.get_user(name = name)
    except Exception as e:
      raise RuntimeError(f"Something goes wrong {str(e)}")
    
    
  def get_role(self, name: str):
    try:
      return self.user_repository.get_role(name=name)
    except Exception as e:
      raise RuntimeError(f"AdminService: something goes wrong: {str(e)}")
    
