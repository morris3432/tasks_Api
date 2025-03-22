# importaciones
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# importar rutas y middlewares
from .routers.users import users
from .routers.OAuth import jwts
from .routers.google import google
from .routers.tasks import task
# from .middlewares.not_found import not_found
# from .middlewares.handles import custom_404

app = FastAPI()

origins = ["*",
           "http://localhost",
           "http://127.0.0.1",
           "exp://192.168.X.X:19000"
           ]

# configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# incluir rutas
app.include_router(users)
app.include_router(jwts)
app.include_router(google)
app.include_router(task)

# middlewares
# app.middleware("http")(not_found)
# app.add_exception_handler(HTTPException, custom_404)


@app.get("/")
async def root():
  return {"message": "Hello World"}
