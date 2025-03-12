from dotenv import load_dotenv
import os

load_dotenv()


class Config():
  port = os.getenv('PORT')

  # MySQL data
  db_user = os.getenv('DB_USER')
  db_password = os.getenv('DB_PASSWORD')
  db_host = os.getenv('DB_HOST')
  db_port = os.getenv('DB_PORT')
  database = os.getenv('DATA_BASE')
