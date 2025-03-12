# importaciones
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from .routers.users import users
from .routers.OAuth import jwts
from .middlewares.not_found import not_found
from .middlewares.handles import custom_404


app = FastAPI()

# incluir rutas
app.include_router(users)
app.include_router(jwts)

# middlewares
app.middleware("http")(not_found)
app.add_exception_handler(HTTPException, custom_404)