from pydantic import BaseModel
from datetime import date

class MateriaSchema(BaseModel):
    name: str
    limite_inscritos: int
    hora_inicio: str
    class Config:
        orm_mode = True

class MateriaResponse(BaseModel):
    id: int
    name: str
    limite_inscritos: int
    hora_inicio: str
    class Config:
        orm_mode = True