from datetime import datetime, timedelta
from typing import Any, Union, Optional

from passlib.context import CryptContext
from jose import jwt


from app.core.config import settings



context = CryptContext(schemes = ["bcrypt"], deprecated="auto")

ALGORTHM = "HS256"

def create_access_token( subject: Union[str, Any] , expire_delta = Optional[datetime])-> str:
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes = settings.ACCESS_TOKEN_EXPIRE
        )
    
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm = ALGORTHM)
    
    return encoded_jwt

def hash_password(password: str)-> str:
    return context.hash(password)

def verify_password(password: str, hashed_password:str)->bool :
    return context.verify(password, hashed_password)

