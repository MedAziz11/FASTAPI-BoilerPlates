from typing import Any
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import json_encoders

from app.apis.crud import user_crud
from app.models.user import User
from app.schemas.user import User as UserResponse, UserCreate, UserUpdate
from app.apis import deps


router = APIRouter()

@router.post('/', response_model = User)
def create_user(
    *,
    db: Session= Depends(deps.get_db),
    user_in: UserCreate,
)-> Any:
    """ Sign up """
    user = user_crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code = 400,
            detail= 'email already exists'
        )
    user = user_crud.user.create(db, obj_in = user_in)
    return user

@router.get("/me/", response_model = User)
def get_current_user(
    *,
    db:Session=Depends(deps.get_db),
    current_user:UserResponse = Depends(deps.get_current_active_user),
)->UserResponse:
    
    return current_user
    
    