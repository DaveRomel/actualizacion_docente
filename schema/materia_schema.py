from pydantic import BaseModel

class MateriaSchema(BaseModel):
    name: str
    limite_inscritos: int
    fecha_curso: str
    hora_inicio: str

class MateriaResponse(BaseModel):
    id: int
    name: str
    limite_inscritos: int
    fecha_curso: str
    hora_inicio: str