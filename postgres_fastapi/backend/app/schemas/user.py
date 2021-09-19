from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name:Optional[str] = None
    

class User(BaseModel):
    id:int
    email:EmailStr
    full_name:Optional[str] = None
    is_active:Optional[bool]
    is_superuser:bool = False
    
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    password: Optional[str] = None