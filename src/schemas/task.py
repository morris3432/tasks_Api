from pydantic import BaseModel

class Task(BaseModel):
  token: str
  title: str
  description: str
  completado: bool
  fecha_iniio: str
  fecha_fin_estimada: str
  fecha_fin_real: str

class TaskU(Task):
  id_task: int