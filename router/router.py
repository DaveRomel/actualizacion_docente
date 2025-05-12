from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED
from schema.user_schema import UserSchema, UserResponse
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
        conn.execute(users.insert().values(new_user))
        print(new_user)
        return new_user

@user.put("/api/user/{user_id}", response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: int):
    with engine.connect() as conn:
        conn.execute(users.update().values(name=data_update.name, username=data_update.username,
        user_passw=data_update.user_passw, email=data_update.email).where(users.c.id == user_id))
        result = conn.execute(users.select().where(users.c.id == id)).first()
        return result