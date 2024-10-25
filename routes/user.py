from fastapi import APIRouter, Response, status
from config.db import conn
from models.user import users
from schemas.user import User
from schemas.userCreate import UserCreate
from cryptography.fernet import Fernet
from starlette.status import HTTP_204_NO_CONTENT
from typing import List

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get("/users", response_model=List[User], tags=["users"])
def get_users():
    result = conn.execute(users.select()).mappings().fetchall()
    print(result)
    if result:
        return result
    else:
        return {"error": "Usuario no encontrado!"}


@user.post("/users", response_model = User, tags=["users"])
def create_user(user: UserCreate):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    print(new_user)
    result = conn.execute(users.insert().values(new_user))
    print(result)
    conn.commit()
    inserted_user = conn.execute(users.select().where(
        users.c.id == result.lastrowid)).fetchone()
    return {
        #accedemos a los elementos
        "id": inserted_user[0], 
        "name": inserted_user[1],
        "email": inserted_user[2],
        "password": inserted_user[3]
    }


@user.get("/users/{id}", response_model=User, tags=["users"])
def get_user(id: str):
    result = conn.execute(users.select().where(
        users.c.id == id)).mappings().fetchone()
    if result:
        return result  # Retornar el resultado como un diccionario
    else:
        return {"error": "Usuario no encontrado!"}


@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    result = conn.execute(users.delete().where(users.c.id == id)).mappings()
    conn.commit()
    if result:
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return "Error al eliminar un usuario"


@user.put("/users/{id}", response_model = User, tags=["users"])
def update_user(id: str, user: User):
    conn.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=f.encrypt(user.password.encode("utf-8"))
    ).where(users.c.id == id))
    updated_user = conn.execute(users.select().where(users.c.id == id)).fetchone()
    
    if update_user:
        return {"id": updated_user[0]}  # Retornar solo el ID del usuario
    else:
        return {"error": "Usuario no encontrado o no se pudo actualizar"}


