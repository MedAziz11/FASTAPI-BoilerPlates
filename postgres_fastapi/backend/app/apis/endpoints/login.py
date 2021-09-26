import secrets
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta


from app.schemas.jwt import JWToken
from app.apis import deps
from app.apis.crud import user_crud
from app.core.config import settings
from app.core.security import create_access_token


router = APIRouter()

@router.post("/access-token/", response_model = JWToken)
def login_access_token(db: Session = Depends(deps.get_db),
                       formData : OAuth2PasswordRequestForm = Depends()):
    """Generates an OAuth token for future use and permissions"""
    user = user_crud.user.authenticate(
        db, email=formData.username, password=formData.password
    )
    if not user:
        HTTPException(status=400, detail="Wrong password or email")
    if not user_crud.user.is_active(user):
        HTTPException(status=400, detail='inactive user')
    access_token_expires = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE)
    response =  {
        "access_token":create_access_token(user.id, access_token_expires),
        "token_type": "bearer"
    }
    return JWToken(**response)