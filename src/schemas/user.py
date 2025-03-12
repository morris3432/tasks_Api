from pydantic import BaseModel


class User(BaseModel):
  username: str
  email: str
  password: str


class UserU(User):
  id_user: int
