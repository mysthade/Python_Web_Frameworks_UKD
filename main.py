import logging

from fastapi import FastAPI, HTTPException, status

from routers import include_routers
from settings.db import ping

logging.basicConfig(level=logging.INFO)

app = FastAPI()
include_routers(app)


@app.get("/")
def index_root():
    return {"message": "Hello World!"}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def db_healthcheck():
    is_alive = await ping()
    if not is_alive:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    return {"status": "healthy", "database": "connected"}
