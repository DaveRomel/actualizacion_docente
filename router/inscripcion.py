from fastapi import APIRouter, HTTPException, Response
from config.db import engine
from models.inscripcion import inscripciones
from models.materias import materias
from models.users import users
from schema.inscripcion_schema import InscripcionSchema, InscripcionResponse, NotificacionInscripcionSchema
from typing import List
from sqlalchemy import select,func
from mailer.email_server import send_email
from starlette.status import HTTP_204_NO_CONTENT

inscripcion = APIRouter()

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
            conn.execute(inscripciones.insert().values(usuario_id=usuario_id, materia_id=materia_id))
            conn.execute(users.update().values(status=1).where(users.c.id == usuario_id))

            #Obtener el usuario y la materia para enviar la notificación
            usuario = conn.execute(users.select().where(users.c.id == usuario_id)).first()
            materia = conn.execute(materias.select().where(materias.c.id == materia_id)).first()
            notificacion_data = NotificacionInscripcionSchema(
                nombre_maestro=usuario.name,
                nombre_curso=materia.name,
                fecha=materia.fecha_curso,
                hora=materia.hora_inicio
            )
            print("datos: ", notificacion_data)
            # Enviar la notificación por correo electrónico
            await enviar_notificacion(notificacion_data, usuario.email)
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al inscribir al usuario: {e}")

        return {"message": "Inscripción exitosa"}

    
@inscripcion.post("/api/inscripcion", response_model=InscripcionResponse)
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
    

async def enviar_notificacion(data: NotificacionInscripcionSchema, email: str):
    try:
        #print(f"Enviando notificación a {nombre} ({email})")
        await send_email("Notificación por inscripción por Correo Electrónico", data, email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {e}")
        
    return Response(status_code = HTTP_204_NO_CONTENT)