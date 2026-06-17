from models.bot_order import BotOrder
from schemas.bot_order import BotOrderCreate, BotOrderUpdate
from services.base import BaseCRUDService, service_dependency


class BotOrderService(BaseCRUDService[BotOrder, BotOrderCreate, BotOrderUpdate]):
    model = BotOrder


get_bot_order_service = service_dependency(BotOrderService)
