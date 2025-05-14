from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED
from schema.user_schema import UserSchema, UserResponse, UserStatus
from config.db import engine
from models.users import users
from werkzeug.security import generate_password_hash,check_password_hash
from typing import List

user = APIRouter()

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
        new_user = data_user.dict()
        with conn.begin():
            conn.execute(users.insert().values(new_user))
            #print(new_user)
        return new_user
        
@user.put("/api/user/{user_id}", response_model=UserResponse)
def update_user(data_update: UserSchema, user_id: int):
    with engine.connect() as conn:
        conn.execute(users.update().values(name=data_update.name, username=data_update.username,
        user_passw=data_update.user_passw, email=data_update.email, celular=data_update.celular,
        procedencia=data_update.procedencia).where(users.c.id == user_id))
        result = conn.execte(users.select().where(users.c.id == user_id)).first()
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
 
