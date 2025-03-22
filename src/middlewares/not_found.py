from fastapi import Request
from fastapi.responses import JSONResponse


async def not_found(r: Request, call_next):
  response = await call_next(r)
  if response.status_code == 404:
    return JSONResponse(
        status_code=404,
        content={
            "status": 404,
            "detail": "Not found"
        },
    )
  return response
