from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer
from ..database.mysql import engine, meta

# tabla de usuarios
user = Table(
    'users',
    meta,
    Column('id_user', Integer, primary_key=True, autoincrement="auto"),
    Column('username', String(255), nullable=False),
    Column('email', String(255), nullable=False),
    Column('password', String(255), nullable=False)
)

meta.create_all(engine)
