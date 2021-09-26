from typing import Optional

from pydantic import BaseModel

class JWToken(BaseModel):
    access_token: str
    token_type: str
    
class JWTData(BaseModel):
    sub: Optional[int]= None