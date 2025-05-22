from fastapi import APIRouter, Depends
from config.db import engine
from models.materias import materias
from schema.materia_schema import MateriaSchema, MateriaResponse
from typing import List
from auth import get_current_active_user

materia = APIRouter(dependencies=[Depends(get_current_active_user)])

@materia.get("/api/materias", response_model=List[MateriaResponse])
def get_materias():
    with engine.connect() as conn:
        result = conn.execute(materias.select()).fetchall()
        return result

@materia.get("/api/materias/{id}", response_model=MateriaResponse)
def get_materia(id: int):
    with engine.connect() as conn:
        result = conn.execute(materias.select().where(materias.c.id == id)).first()
        return result

@materia.post("/api/materias", response_model=MateriaResponse)
def create_materia(data_materia: MateriaSchema):
    with engine.connect() as conn:
        new_materia = data_materia.dict()
        with conn.begin():
            result = conn.execute(materias.insert().values(new_materia))
            conn.commit()
            new_materia["id"] = result.lastrowid
        return new_materia

@materia.put("/api/materias/{materia_id}", response_model=MateriaResponse)
def update_materia(data_update: MateriaSchema, materia_id: int):
    with engine.connect() as conn:
        conn.execute(materias.update().values(name=data_update.name, limite_inscritos=data_update.limite_inscritos, fecha_curso=data_update.fecha_curso, hora_inicio=data_update.hora_inicio).where(materias.c.id == materia_id))
        result = conn.execute(materias.select().where(materias.c.id == materia_id)).first()
        conn.commit()
        return result

@materia.delete("/api/materias/{materia_id}")
def delete_materia(materia_id: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(materias.delete().where(materias.c.id == materia_id))
            return {"message": "Materia eliminada correctamente"}