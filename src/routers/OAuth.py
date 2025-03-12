from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from sqlalchemy import and_
import jwt
import json
# db
from ..database.mysql import conn
from ..models.sessions import sessions
from ..models.user import user

jwts = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

SECRET_KEY = "WAS256KHLI85"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

Oauth2 = OAuth2PasswordBearer(tokenUrl="/")
now = datetime.now()
future = now + timedelta(days=7)


def serch_user(username: str, password: str):
  resp = conn.execute(
      user.select().where(
          and_(
              user.c.username == username,
              user.c.password == password
          )
      )
  ).mappings().fetchone()
  if not resp:
    return False
  return resp


def token(data: dict, expire: timedelta | None = None):
  toEncode = data.copy()
  expira = datetime.now() + (expire or timedelta(minutes=15))
  toEncode.update({'exp': expira})

  token = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)

  if len(token) > 255:
    token = token[:255]

  return token


@jwts.post("/")
def login(form: OAuth2PasswordRequestForm = Depends()):
  users = serch_user(username=form.username, password=form.password)

  if not users:
    raise HTTPException(
        status_code=404,
        detail="Credenciale invalidas"
    )

  users = {key: value for key, value in users.items() if key != 'password'}

  acces_token = token(data={"sub": users["username"]}, expire=timedelta(
      minutes=ACCESS_TOKEN_EXPIRE))
  session = {
      "token": acces_token,
      "id_user": users["id_user"],
      "fecha_login": now.strftime("%Y-%m-%d"),
      "fecha_loup": None,
      "fecha_fin_expira": future.strftime("%Y-%m-%d"),
  }

  conn.execute(sessions.insert().values(session))
  conn.commit()

  res = [{**users, **session}]
  # respuesta
  return {
      "status": "success",
      "row": len(res),
      "data": jsonable_encoder(res)
  }
