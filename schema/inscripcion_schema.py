from pydantic import BaseModel

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
    fecha: str
    hora: str
    class Config:
        orm_mode = True