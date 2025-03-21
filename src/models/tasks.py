from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Date, Boolean, Text
# metadata y engine
from ..database.mysql import meta, engine

# tabla de tareas
tasks = Table(
  "tasks",
  meta,
  Column("id_task", Integer, primary_key=True, autoincrement="auto"),
  Column("id_user",Integer, ForeignKey("users.id_user"), nullable=False),
  Column("title",String(100),nullable=False),
  Column("description",Text,nullable=False),
  Column("completado",Boolean,nullable=False),
  Column("fecha_iniio",Date,nullable=False),
  Column("fecha_fin_estimada",Date,nullable=False),
  Column("fecha_fin_real",Date,nullable=True)
)

# creacion de la tabla
meta.create_all(engine)