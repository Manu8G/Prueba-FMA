from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from enum import Enum

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class estadoTarea(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"

import logging
import git
import os
actual_path = os.path.abspath(__file__)
repo = git.Repo(search_parent_directories=True, path=actual_path)
path_repo = repo.git.rev_parse("--show-toplevel")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt