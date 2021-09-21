from typing import Optional
from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str

    

class User(UserBase):
    id: Optional[str] = None
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    password: Optional[str] = None