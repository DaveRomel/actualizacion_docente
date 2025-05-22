from pydantic import BaseModel, Field
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
    codigo_recuperacion: Optional[str] = None
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
    codigo_recuperacion: Optional[str] = None

class UserStatus(BaseModel):
    status: int

class RecuperacionEmailSchema(BaseModel):
    name: str
    codigo: str
    email: str

class CambioContrasenaSchema(BaseModel):
    email: str
    codigo: str = Field(..., min_length=6, max_length=6)
    nuevo_password: str = Field(..., min_length=8)
    confirmar_password: str = Field(..., min_length=8)
