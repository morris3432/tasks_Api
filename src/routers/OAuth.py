import secrets
import string
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import and_
from ..database.mysql import conn
from ..models.sessions import sessions
from ..models.user import user
from ..config.config import Config

jwts = APIRouter(
  prefix="/auth",
  tags=["Auth"],
)

config = Config()
now = datetime.now()
future = now + timedelta(days=7)

def generate_token(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def search_user(email: str, password: str):
  resp = conn.execute(
    user.select().where(
    user.c.email == email, user.c.password == password
    )
  ).mappings().fetchone()
  if not resp:
    conn.rollback()
    return False
    
  return resp

@jwts.post("/")
def login(form: OAuth2PasswordRequestForm = Depends()):
    users = search_user(email=form.username, password=form.password)

    if not users:
        raise HTTPException(
            status_code=404,
            detail="Credenciales inválidas"
        )

    users = {key: value for key, value in users.items() if key != 'password'}

    # Genera un token aleatorio de 8 caracteres
    access_token = generate_token(8)
    
    session = {
        "token": access_token,
        "id_user": users["id_user"],
        "fecha_login": now.strftime("%Y-%m-%d"),
        "fecha_loup": None,
        "fecha_fin_expira": future.strftime("%Y-%m-%d"),
    }

    conn.execute(sessions.insert().values(session))
    conn.commit()

    res = [{**users, **session}]
    
    return {
        "status": "success",
        "row": len(res),
        "data": res
    }
