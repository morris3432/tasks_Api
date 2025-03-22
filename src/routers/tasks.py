from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from datetime import datetime
# datos de conexión
from ..database.mysql import conn
from ..models.tasks import tasks
from ..models.sessions import sessions
from ..schemas.task import Task, TaskU

task = APIRouter(
    prefix="/tasks",
    tags=["Tareas"],
)

now = datetime.now()
format_day = now.strftime("%Y-%m-%d")


@task.get("/{token}", description="Obtener tareas según el token")
def get_tasks(token: str):
  try:
    sesion = conn.execute(
        sessions.select()
        .where(sessions.c.token == token)
    ).mappings().fetchone()

    if sesion["fecha_fin_expira"] == format_day:
      raise HTTPException(
          status_code=401,
          detail="Token expirado"
      )

    id_user = sesion["id_user"]
    tareas = conn.execute(
        tasks.select()
        .where(tasks.c.id_user == id_user)
    ).fetchall()
    
    conn.closed()

    response = [
        dict(res._mapping)
        for res in tareas
    ]

    return {
        "status": "success",
        "row": len(response),
        "data": jsonable_encoder(response)
    }

  except Exception as e:
    conn.rollback()
    raise HTTPException(
        status_code=500,
        detail=str(e)
    )


@task.post("/", description="Crea una nueva tarea")
def new_task(data: Task):
  try:
    sesion = conn.execute(
        sessions.select()
        .where(sessions.c.token == data.token)
    ).mappings().fetchone()

    # Verificar si no se encontró la sesión
    if sesion is None:
      raise HTTPException(
          status_code=404,
          detail="Token no encontrado"
      )

    # Comparar las fechas como strings
    if sesion["fecha_fin_expira"] == format_day:
      raise HTTPException(
          status_code=401,
          detail="Token expirado"
      )

    id_user = sesion["id_user"]
    dicts = {
        "id_user": id_user,
        "title": data.title,
        "description": data.description,
        "completado": data.completado,
        "fecha_iniio": data.fecha_iniio,
        "fecha_fin_estimada": data.fecha_fin_estimada,
        "fecha_fin_real": data.fecha_fin_real,
    }

    conn.execute(tasks.insert().values(dicts))
    conn.commit()
    
    conn.closed()

    return {
        "status": "OK",
        "message": "Tarea creada con éxito",
    }
  except Exception as e:
    conn.rollback()
    raise HTTPException(
        status_code=500,
        detail=str(e)
  )