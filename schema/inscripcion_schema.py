from pydantic import BaseModel
from datetime import date

class InscripcionSchema(BaseModel):
    usuario_id: int
    materia_id: int
    class Config:
        orm_mode = True

class InscripcionResponse(BaseModel):
    id: int
    usuario_id: int
    materia_id: int
    class Config:
        orm_mode = True

class NotificacionInscripcionSchema(BaseModel):
    nombre_maestro: str
    nombre_curso: str
    hora: str
    fecha: str
    class Config:
        orm_mode = True