from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from datetime import datetime, timedelta
import jwt
import requests
import random

# conexión a la base de datos
from ..database.mysql import conn
from ..models.user import user
from ..models.sessions import sessions
from ..utils.send_email import send_email
from ..config.config import Config

config = Config()
# datos para autenticación
CLIENT_ID = config.client_id
CLIENT_SECRET = config.client_secret
REDIRECT_URI = config.redirect_uri #<- redirección (cambia en produción)
GOOGLE_AUTH_URL = config.google_auth_url
GOOGLE_TOKEN_URL = config.google_token_url
GOOGLE_USERINFO_URL = config.google_userinfo_url
SECRET_KEY = config.secret_key
ALGORITHM = config.algorithm
ACCESS_TOKEN_EXPIRE = config.access_token_expire

# ruta principal
google = APIRouter(
  prefix='/google',
  tags=['Auth con Google']
)

# autenticación con Google
oauth2 = OAuth2AuthorizationCodeBearer(
  authorizationUrl=GOOGLE_AUTH_URL,
  tokenUrl=GOOGLE_TOKEN_URL
)

# Random password generator
def password_random():
  return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

# Buscar usuario
def search_user(email: str):
  user_data = conn.execute(user.select().where(user.c.email == email)).mappings().fetchone()
  return user_data
# fecha
now = datetime.now()
future = now+timedelta(days=7)

# lleva a la autenticación con Google y obtiene el token para la autenticación
@google.get("/")
def login_google():
  params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": "openid email profile",
    "access_types": "offline",
    "prompt": "consent"
  }
  google_url= f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
  return RedirectResponse(google_url)

# obtiene el token y la información del usuario    
@google.get("/callback")
def callback(code: str):
  data = {
    "code": code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
  }

  token_res = requests.post(url=GOOGLE_TOKEN_URL, data=data)

  if token_res.status_code != 200:
    raise HTTPException(
      status_code=400,
      detail="Error al obtener el token de Google"
    )
    
  token_data = token_res.json()
  access_token = token_data["access_token"]
  user_res = requests.get(
    GOOGLE_USERINFO_URL,
    headers={"Authorization": f"Bearer {access_token}"}
  )
    
  if user_res.status_code != 200:
    raise HTTPException(
      status_code=400,
      detail="Error al obtener la información del usuario de Google"
    )
    
  user_info = user_res.json()    
  email = user_info["email"]
  username = user_info.get("name", email.split("@")[0])
  user_data = search_user(email)
    
  json_response = {}
    
  # Busca el usuario en la base de datos y si no lo encuentra lo crea
  if not user_data:
    json_response = {
      "username": username,
      "email": email,
      "password": password_random()
    }
    res = conn.execute(user.insert().values(json_response))
    conn.commit()
    select = conn.execute(user.select().where(user.c.id_user == res.lastrowid)).mappings().fetchone()
    json_response["id_user"] = select["id_user"]
    del json_response["password"]
  else:
    json_response = {
    "id_user": user_data["id_user"],
    "username": user_data["username"],
    "email": user_data["email"]
  }
    
    # crea un token
  token = jwt.encode(
    {
      "sub": json_response["username"],
      "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    },
    SECRET_KEY,
    algorithm=ALGORITHM
  )
    
  # verifica el tamaño del token
  if len(token) > 255:
    token = token[:255]
    
  # crea la sesion para la tabla sessions con el id del usuario
  sesion = {
    "token": token,
    "id_user": json_response["id_user"],
    "fecha_login": now.strftime("%Y-%m-%d"),
    "fecha_loup": None,
    "fecha_fin_expira": future.strftime("%Y-%m-%d")
  }
    
  # guarda la sesion
  conn.execute(sessions.insert().values(sesion))
  conn.commit()
    
  datas=[{**json_response,**sesion}]
    
    # responde con una lista de diccionarios con la información del usuario
  return {
    "status": "SUCCESS",
    "data":jsonable_encoder(datas)
  }
