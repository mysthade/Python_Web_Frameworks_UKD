import logging

from fastapi import FastAPI, HTTPException, status

from routers.bot_features import router as bot_features_router
from routers.bot_orders import router as bot_orders_router
from routers.files import router as files_router
from routers.invoices import router as invoices_router
from routers.order_to_features import router as order_to_features_router
from routers.profiles import router as profiles_router
from routers.users import router as users_router
from settings.db import ping

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(users_router)
app.include_router(profiles_router)
app.include_router(bot_features_router)
app.include_router(bot_orders_router)
app.include_router(invoices_router)
app.include_router(order_to_features_router)
app.include_router(files_router)


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
