from dotenv import load_dotenv
import os

load_dotenv()


class Config():
  port = int(os.getenv('PORT'))

  # MySQL data
  db_user = str(os.getenv('DB_USER'))
  db_password = str(os.getenv('DB_PASSWORD'))
  db_host = str(os.getenv('DB_HOST'))
  db_port = str(os.getenv('DB_PORT'))
  database = str(os.getenv('DATA_BASE'))

  # Gmail
  correo = str(os.getenv("MAIL"))
  clave = str(os.getenv("PASSWORD"))

  # OAth2
  client_id = str(os.getenv("CLIENT_ID"))
  client_secret = str(os.getenv("CLIENT_SECRET"))
  redirect_uri = str(os.getenv("REDIRECT_URI"))
  google_auth_url = str(os.getenv("GOOGLE_AUTH_URL"))
  google_token_url = str(os.getenv("GOOGLE_TOKEN_URL"))
  google_userinfo_url = str(os.getenv("GOOGLE_USERINFO_URL"))
  secret_key = str(os.getenv("SECRET_KEY"))
  algorithm = str(os.getenv("ALGORITHM"))
  access_token_expire = int(os.getenv("ACCESS_TOKEN_EXPIRE"))