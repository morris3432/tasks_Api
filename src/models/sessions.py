from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Date
# metadata y engine
from ..database.mysql import meta, engine

# tabla
sessions = Table(
    'sessions',
    meta,
    Column('token', String(255), nullable=False),
    Column('id_user', Integer, ForeignKey("users.id_user"), nullable=False,),
    Column('fecha_login', Date, nullable=False),
    Column('fecha_loup', Date, nullable=True),
    Column('fecha_fin_expira', Date, nullable=False)
)

# creacion de la tabla
meta.create_all(engine)
