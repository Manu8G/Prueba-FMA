from src.repository.user_repository import UserRepository

class UserService:
  def __init__(self):
    self.user_repository = UserRepository()

  
  def get_user(self, id_user: str):
    try:
      return self.user_repository.get_user(id_user)
    except Exception as e:
      raise RuntimeError(f"Something goes wrong {str(e)}")
    
    
  async def get_role(self, id: str):
    try:
      return await self.user_repository.get_role(id)
    except Exception as e:
      raise RuntimeError(f"AdminService: something goes wrong: {str(e)}")
    
    
  async def get_user_info(self, id: str):
    try:
      return await self.user_repository.get_user_info(id)
    except Exception as e:
      raise RuntimeError(f"AdminService: something goes wrong: {str(e)}")  
