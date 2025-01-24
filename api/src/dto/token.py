from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    id: str

class TokenData(BaseModel):
    name: Optional[str] = None