from sqlalchemy.sql.expression import true
from pydantic import BaseModel
from datetime import datetime

class PostSchema(BaseModel):
    title: str
    author: str
    content: str
    
class PostResponse(BaseModel):
    id: int
    title: str
    author: str
    content: str
    time_created: datetime
    
    class Config:
        orm_mode = True