from fastapi import APIRouter, FastAPI

from routers.auth import router as auth_router
from routers.bot_features import router as bot_features_router
from routers.bot_orders import router as bot_orders_router
from routers.files import router as files_router
from routers.invoices import router as invoices_router
from routers.order_to_features import router as order_to_features_router
from routers.profiles import router as profiles_router
from routers.users import router as users_router

API_ROUTERS: list[APIRouter] = [
    users_router,
    auth_router,
    profiles_router,
    bot_features_router,
    bot_orders_router,
    invoices_router,
    order_to_features_router,
    files_router,
]


def include_routers(app: FastAPI) -> None:
    for router in API_ROUTERS:
        app.include_router(router)
