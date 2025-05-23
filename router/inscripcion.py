from fastapi import APIRouter, HTTPException, Response, Depends
from config.db import engine
from models.inscripcion import inscripciones
from models.materias import materias
from models.users import users
from schema.inscripcion_schema import InscripcionSchema, InscripcionResponse, NotificacionInscripcionSchema
from typing import List
from sqlalchemy import select,func
from mailer.email_server import send_email
from starlette.status import HTTP_204_NO_CONTENT
from auth import get_current_active_user

inscripcion = APIRouter(dependencies=[Depends(get_current_active_user)])

@inscripcion.get("/api/inscripcion", response_model=List[InscripcionResponse])
def get_inscripcion():
    with engine.connect() as conn:
        result = conn.execute(inscripciones.select()).fetchall()
        return result
    
    
@inscripcion.post("/api/inscripcion/{usuario_id}/{materia_id}")
async def inscribir_usuario(usuario_id: int, materia_id: int):
    with engine.connect() as conn:
        # Verificar si el usuario ya está inscrito en una materia
        user_inscrito = conn.execute(select(users.c.status).select_from(users).where(users.c.id == usuario_id)).scalar()        
        if user_inscrito:
            raise HTTPException(status_code=400, detail="Usuario ya inscrito en una materia")
        
        inscritos = conn.execute(select(func.count()).select_from(inscripciones).where(inscripciones.c.materia_id == materia_id)).scalar()
        limite_inscritos = conn.execute(select(materias.c.limite_inscritos).select_from(materias).where(materias.c.id == materia_id)).scalar()

        #print(inscritos)
        #print(limite_inscritos)
        if inscritos >= limite_inscritos:
            raise HTTPException(status_code=400, detail="No se puede inscribir, el límite de inscritos ha sido alcanzado")

        try:
            correoEnviado = conn.execute(select(users.c.correoEnviado).select_from(users).where(users.c.id == usuario_id)).scalar()        
            conn.execute(inscripciones.insert().values(usuario_id=usuario_id, materia_id=materia_id))

            conn.execute(users.update().values(status=materia_id, correoEnviado=1).where(users.c.id == usuario_id))

            #Obtener el usuario y la materia para enviar la notificación
            usuario = conn.execute(users.select().where(users.c.id == usuario_id)).first()
            materia = conn.execute(materias.select().where(materias.c.id == materia_id)).first()
            notificacion_data = NotificacionInscripcionSchema(
                nombre_maestro=usuario.name,
                nombre_curso=materia.name,
                fecha=materia.fecha_curso,
                hora=materia.hora_inicio
            )
            # Enviar la notificación por correo electrónico
            if correoEnviado == 0:
                await send_email(
                    subject="Notificación por inscripción por Correo Electrónico", 
                    data=notificacion_data,
                    email=usuario.email, 
                    template_file="email_template.html"
                )
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al inscribir al usuario: {e}")

        return {"message": "Inscripción exitosa"}

    
#@inscripcion.post("/api/inscripcion", response_model=InscripcionResponse)
def create_inscripcion(inscripcion: InscripcionSchema):
    with engine.connect() as conn:
        result = conn.execute(inscripciones.insert().values(usuario_id=inscripcion.usuario_id, materia_id=inscripcion.materia_id))
        conn.commit()
        return {"id": result.inserted_primary_key[0], "usuario_id": inscripcion.usuario_id, "materia_id": inscripcion.materia_id}
    
@inscripcion.get("/api/inscripcion/{materia_id}")
def ver_inscripciones_por_materia(materia_id: int):
    with engine.connect() as conn:
        result = conn.execute(inscripciones.select().where(inscripciones.c.materia_id == materia_id)).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron inscripciones para esta materia")
        result = [{"usuario_id": row.usuario_id, "materia_id": row.materia_id} for row in result]
        return result

@inscripcion.get("/api/inscripcion/contar_inscritos_por_materia/{materia_id}")
def contar_inscritos(materia_id: int):
    with engine.connect() as conn:
        result = select(func.count()).select_from(inscripciones).where(inscripciones.c.materia_id == materia_id)
        inscritos = conn.execute(result).scalar()
        return inscritos

@inscripcion.delete("/api/inscripcion/{usuario_id}")
def delete_inscripcion(usuario_id: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(inscripciones.delete().where(inscripciones.c.usuario_id == usuario_id))
            conn.execute(users.update().values(status=0).where(users.c.id == usuario_id))
            conn.commit()
            return {"message": "Inscripción eliminada correctamente"}