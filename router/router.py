from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_204_NO_CONTENT
from schema.user_schema import UserSchema, UserResponse, UserStatus, RecuperacionEmailSchema, CambioContrasenaSchema, UserCreate, UserUpdate
from config.db import engine
from models.users import users
from werkzeug.security import generate_password_hash,check_password_hash
from typing import List
from passlib.context import CryptContext
from auth import get_current_active_user
import random
from mailer.email_server import send_email

user = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


@user.get("/user")
def get_user(): 
    return {"message": "Este es la raiz de router"}


@user.get("/api/user", response_model=List[UserResponse])
def get_users(current_user: UserResponse = Depends(get_current_active_user)):
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result
    
@user.get("/api/user/{id}", response_model=UserResponse)
def get_user(id: int, current_user: UserResponse = Depends(get_current_active_user)):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == id)).first()
        return result
    
@user.post("/api/user")
def create_user(data_user: UserCreate):
    with engine.connect() as conn:
        # Hash the password
        hashed_password = get_password_hash(data_user.user_passw)
        
        new_user = {
            "status": 0,
            "name": data_user.name,
            "email": data_user.email,
            "celular": data_user.celular,
            "user_passw": hashed_password,
            "procedencia": data_user.procedencia,
            "correoEnviado": 0
        }
        with conn.begin():
            conn.execute(users.insert().values(new_user))
            #print(new_user)
        return new_user
        
@user.put("/api/user/{user_id}", response_model=UserResponse)
def update_user(data_update: UserUpdate, user_id: int, current_user: UserResponse = Depends(get_current_active_user)):
    with engine.connect() as conn:
        conn.execute(users.update().values(name=data_update.name, 
        email=data_update.email, celular=data_update.celular,
        procedencia=data_update.procedencia).where(users.c.id == user_id))
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        conn.commit()
        return result

@user.put("/api/user_status_0/{user_id}", response_model=UserResponse)
def downgrade_status(user_id: int, current_user: UserResponse = Depends(get_current_active_user)):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(users.update().values(status='0').where(users.c.id == user_id))
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            return result
        
@user.put("/api/user_status_1/{user_id}", response_model=UserResponse)
def upgrade_status_1(user_id: int, current_user: UserResponse = Depends(get_current_active_user)):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(users.update().values(status='1').where(users.c.id == user_id))
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            print(f'Enviando notificación a {result.name} ({result.email})')
            # Enviar notificación por correo electrónico
            return result
        
@user.put("/api/user_status_2/{user_id}", response_model=UserResponse)
def upgrade_status_2(user_id: int, current_user: UserResponse = Depends(get_current_active_user)):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(users.update().values(status='2').where(users.c.id == user_id))
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            return result
        
@user.put("/api/user_status_3/{user_id}", response_model=UserResponse)
def upgrade_status_3(user_id: int, current_user: UserResponse = Depends(get_current_active_user)):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(users.update().values(status='3').where(users.c.id == user_id))
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            return result
 
@user.post("/api/recuperar")
async def recuperar_password(email: str):
    with engine.connect() as conn:
        try:
            # Verificar si el correo electrónico existe en la base de datos
            user = conn.execute(users.select().where(users.c.email == email)).first()
            if not user:
                return {"message": "El correo electrónico no está registrado."}
            
            # Generar un nuevo código de recuperación
            codigo = str(random.randint(100000, 999999))  # Código de 6 dígitos

            # Actualizar el código de recuperación en la base de datos
            conn.execute(users.update().values(codigo_recuperacion=codigo).where(users.c.email == email))
            data = RecuperacionEmailSchema(
                name=user.name,
                codigo=codigo,
                email=email
            )

            await send_email(
                subject="Recuperación de contraseña",
                data=data,
                email=email,
                template_file="codigo_recuperacion.html"  
            )
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {e}")
        return {"message": "Se ha enviado un código de recuperación a tu correo electrónico."}

@user.put("/api/cambiar_contrasena")
def cambiar_contrasena(data: CambioContrasenaSchema):
    with engine.connect() as conn:
        try:
            # Verificar si las contraseñas coinciden
            if data.nuevo_password != data.confirmar_password:
                raise HTTPException(status_code=400, detail="Las contraseñas no coinciden.")
            
            # Buscar si el usuario existe
            user = conn.execute(users.select().where(users.c.email == data.email)).first()
            if not user:
                raise HTTPException(status_code=400, detail="Usuario no existe.")
            
            if data.codigo != user.codigo_recuperacion:
                raise HTTPException(status_code=400, detail="Código de recuperación incorrecto.")
            
            # Actualizar la contraseña en la base de datos
            hashed_password = get_password_hash(data.nuevo_password)
            conn.execute(users.update().values(user_passw=hashed_password).where(users.c.email == data.email))
            conn.commit()
            
            return {"message": "Contraseña actualizada exitosamente."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al cambiar la contraseña: {e}")