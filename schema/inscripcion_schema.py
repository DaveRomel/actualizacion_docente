from pydantic import BaseModel

class InscripcionSchema(BaseModel):
    usuario_id: int
    materia_id: int

class InscripcionResponse(BaseModel):
    id: int
    usuario_id: int
    materia_id: int

class NotificacionInscripcionSchema(BaseModel):
    nombre_maestro: str
    nombre_curso: str
    fecha: str
    hora: str