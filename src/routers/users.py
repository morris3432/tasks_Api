from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
# datos de conexión
from ..database.mysql import conn
from ..models.user import user
from ..schemas.user import User, UserU

users = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@users.post("/", description="Crea un nuevo usuario")
def new_user(data: User):
  try:
    dicts = {
        "username": data.username,
        "email": data.email,
        "password": data.password
    }
    conn.execute(user.insert().values(dicts))
    conn.commit()

    return {
        "status": "OK",
        "message": "Usuario creado con exito",
    }
  except Exception as e:
    conn.rollback()
    raise {"status": "ERROR", "message": str(e)}


@users.put("/", description="Actualiza un usurio")
def update_user(data: UserU):
  try:
    exist = conn.execute(user.select().where(
        user.c.id_user == data.id_user)).fetchone()

    if not exist:
      raise HTTPException(status_code=404, detail="Usuario no encontrado")

    dicts = {
        "username": data.username,
        "email": data.email,
        "password": data.password
    }
    conn.execute(user.update().where(
        user.c.id_user == data.id_user).values(dicts))
    conn.commit()

    return {
        "status": "OK",
        "message": "Usuario actualizado con exito",
    }
  except Exception as e:
    raise {"status": "ERROR", "message": str(e)}


@users.delete("/{id}", description="Elimina un usuario")
def delete_user(id):
  try:
    exist = conn.execute(user.select().where(user.c.id_user == id)).fetchone()
    if not exist:
      raise HTTPException(status_code=404, detail="Usuario no encontrado")

    conn.execute(user.delete().where(user.c.id_user == id))
    conn.commit()
    return {
        "status": "OK",
        "message": "Usuario eliminado con exito",
    }
  except Exception as e:
    raise {"status": "ERROR", "message": str(e)}
