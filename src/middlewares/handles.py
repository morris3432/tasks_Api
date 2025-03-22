from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


async def custom_404(request: Request, exc: HTTPException):
  if exc.status_code == 404:
    return JSONResponse(
        status_code=404,
        content={
            "status": "ERROR",
            "message": "Ruta no encontrada",
            "details": str(exc.detail)
        }
    )
  return JSONResponse(
      status_code=exc.status_code,
      content={
          "status": "ERROR",
          "message": str(exc.detail)
      }
  )
