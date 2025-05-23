from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    celular: str
    user_passw: str
    procedencia: str
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: str
    celular: str
    procedencia: str
    email: str
    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    #id: Optional[int] = None
    name: str
    email: str
    status: int
    celular: str
    user_passw: str
    procedencia: str
    correoEnviado: int
    codigo_recuperacion: Optional[str] = None
    class Config:
        orm_mode = True
    #class Config:
    #    from_attributes = True
        
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    status: int
    celular: str
    user_passw: str
    procedencia: str
    correoEnviado: int
    codigo_recuperacion: Optional[str] = None
    class Config:
        orm_mode = True

class UserStatus(BaseModel):
    status: int
    class Config:
        orm_mode = True

class RecuperacionEmailSchema(BaseModel):
    name: str
    codigo: str
    email: str
    class Config:
        orm_mode = True

class CambioContrasenaSchema(BaseModel):
    email: str
    codigo: str = Field(..., min_length=6, max_length=6)
    nuevo_password: str = Field(..., min_length=8)
    confirmar_password: str = Field(..., min_length=8)
    class Config:
        orm_mode = True
