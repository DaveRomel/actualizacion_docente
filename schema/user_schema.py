from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    #id: Optional[int] = None
    name: str
    username: str
    user_passw: str
    email: str
    status: int
    #class Config:
    #    from_attributes = True
        
class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    user_passw: str
    email: str
    status: int
