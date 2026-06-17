from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.bot_order import BotOrder
from schemas.bot_order import BotOrderCreate, BotOrderUpdate
from settings.db import get_db


class BotOrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[BotOrder]:
        result = await self.db.execute(select(BotOrder))
        return result.scalars().all()

    async def get_by_id(self, order_id: int) -> BotOrder | None:
        return await self.db.get(BotOrder, order_id)

    async def create(self, data: BotOrderCreate) -> BotOrder:
        order = BotOrder(**data.model_dump())
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def update(self, order_id: int, data: BotOrderUpdate) -> BotOrder | None:
        order = await self.get_by_id(order_id)
        if not order:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(order, key, value)
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def delete(self, order_id: int) -> bool:
        order = await self.get_by_id(order_id)
        if not order:
            return False
        await self.db.delete(order)
        await self.db.commit()
        return True


async def get_bot_order_service(
    db: AsyncSession = Depends(get_db),
) -> BotOrderService:
    return BotOrderService(db)
