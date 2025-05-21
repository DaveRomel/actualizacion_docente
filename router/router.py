from fastapi import APIRouter, Response, HTTPException
from starlette.status import HTTP_201_CREATED
from schema.user_schema import UserSchema, UserResponse, UserStatus
from config.db import engine
from models.users import users
from werkzeug.security import generate_password_hash,check_password_hash
from typing import List
from passlib.context import CryptContext


user = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


@user.get("/user")
def get_user(): 
    return {"message": "Este es la raiz de router"}


@user.get("/api/user", response_model=List[UserResponse])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result
    
@user.get("/api/user/{id}", response_model=UserResponse)
def get_user(id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == id)).first()
        return result
    
@user.post("/api/user")
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        # Hash the password
        hashed_password = get_password_hash(data_user.user_passw)
        
        new_user = {
            "status": 0,
            "name": data_user.name,
            "email": data_user.email,
            "celular": data_user.celular,
            "username": data_user.username,
            "user_passw": hashed_password,
            "procedencia": data_user.procedencia,
            "correoEnviado": 0
        }
        with conn.begin():
            conn.execute(users.insert().values(new_user))
            #print(new_user)
        return new_user
        
@user.put("/api/user/{user_id}", response_model=UserResponse)
def update_user(data_update: UserSchema, user_id: int):
    with engine.connect() as conn:
        conn.execute(users.update().values(name=data_update.name, username=data_update.username,
        user_passw=data_update.user_passw, email=data_update.email, celular=data_update.celular,
        procedencia=data_update.procedencia, correoEnviado=data_update.correoEnviado).where(users.c.id == user_id))
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        conn.commit()
        return result

@user.put("/api/user_status_0/{user_id}", response_model=UserResponse)
def downgrade_status(user_id: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(users.update().values(status='0').where(users.c.id == user_id))
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            return result
        
@user.put("/api/user_status_1/{user_id}", response_model=UserResponse)
def upgrade_status_1(user_id: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(users.update().values(status='1').where(users.c.id == user_id))
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            print(f'Enviando notificación a {result.name} ({result.email})')
            # Enviar notificación por correo electrónico
            return result
        
@user.put("/api/user_status_2/{user_id}", response_model=UserResponse)
def upgrade_status_2(user_id: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(users.update().values(status='2').where(users.c.id == user_id))
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            return result
        
@user.put("/api/user_status_3/{user_id}", response_model=UserResponse)
def upgrade_status_3(user_id: int):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(users.update().values(status='3').where(users.c.id == user_id))
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            return result
 

