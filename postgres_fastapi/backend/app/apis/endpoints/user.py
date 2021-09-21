from typing import Any
from pydantic import EmailStr
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from app.apis.crud import user_crud
from app.models.user import User
from app.schemas.user import User as UserResponse, UserCreate, UserUpdate
from app.apis import deps


router = APIRouter()

@router.post('/', response_model = UserResponse)
def create_user(
    *,
    db: Session= Depends(deps.get_db),
    user_in: UserCreate
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

# @router.get("/me/", response_model = User)
# def get_current_user(
#     *,
#     db:Session=Depends(deps.get_db),
#     current_user:UserResponse = Depends(deps.get_current_active_user),
# )->UserResponse:
    
#     return current_user

# @router.put("/", response_model=User)
# def update_active_current_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     password: str = Body(None),
#     full_name: str = Body(None),
#     email: EmailStr = Body(None),
#     current_user: User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update user.
#     """
#     current_user_data = jsonable_encoder(current_user)
#     user_in = UserUpdate(**current_user_data)
#     if password is not None:
#         user_in.password = password
#     if full_name is not None:
#         user_in.full_name = full_name
#     if email is not None:
#         user_in.email = email
#     user = user_crud.user.update(db, db_obj=current_user, obj_in=user_in)
#     return user
    
    