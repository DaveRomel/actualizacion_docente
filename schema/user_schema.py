from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    #id: Optional[int] = None
    name: str
    email: str
    status: int
    celular: str
    username: str
    user_passw: str
    procedencia: str
    correoEnviado: int
    #class Config:
    #    from_attributes = True
        
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    status: int
    celular: str
    username: str
    user_passw: str
    procedencia: str
    correoEnviado: int

class UserStatus(BaseModel):
    status: int
