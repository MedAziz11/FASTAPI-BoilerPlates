from typing import Optional

from datetime import timedelta

from pydantic import BaseModel

class JWToken(BaseModel):
    access_token: str
    token_type: str
    expires: timedelta
    
class JWTData(BaseModel):
    sub: Optional[int]= None