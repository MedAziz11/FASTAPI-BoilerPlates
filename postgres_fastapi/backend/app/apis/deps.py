from sqlalchemy.sql.functions import current_user
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.jwt import JWTData
from app.core.config import settings
from app.core import security
from app.apis.crud import user_crud

from sqlalchemy.orm.session import Session
from typing import Generator
from jose import jwt
from pydantic import ValidationError

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException



oauth2_token = OAuth2PasswordBearer(
    tokenUrl= "/login/access-token"
)

def get_db()-> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_token)
)-> User:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, algorithms = [security.ALGORTHM]
            )
        token_data = JWTData(**payload)     
        
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="invalid credentials"
        )
    user = user_crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    return user


def get_current_active_user(user: User= Depends(get_current_user)):
    if not user.is_active(current_user):
        raise HTTPException(status=404, detail="Inactive User")
    return user

