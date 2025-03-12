from sqlalchemy import MetaData, create_engine
from ..config.config import Config

# configuracion
config = Config()

# MySQL
user = config.db_user
password = config.db_password
host = config.db_host
port = config.db_port
db = config.database

# link
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
)
conn = engine.connect()
# meta
meta = MetaData()
