from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from models.bot_order import BotOrderStatus


class BotOrderCreate(BaseModel):
    title: str
    description: str
    status: BotOrderStatus
    price: Decimal
    client_id: int


class BotOrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: BotOrderStatus
    price: Decimal
    client_id: int


class BotOrderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BotOrderStatus] = None
    price: Optional[Decimal] = None
    client_id: Optional[int] = None
