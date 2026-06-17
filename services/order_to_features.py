from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.order_to_feature import OrderToFeature
from schemas.order_to_feature import OrderToFeatureCreate
from settings.db import get_db


class OrderToFeatureService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[OrderToFeature]:
        result = await self.db.execute(select(OrderToFeature))
        return result.scalars().all()

    async def get_by_id(self, order_id: int, feature_id: int) -> OrderToFeature | None:
        return await self.db.get(OrderToFeature, (order_id, feature_id))

    async def create(self, data: OrderToFeatureCreate) -> OrderToFeature:
        link = OrderToFeature(**data.model_dump())
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def delete(self, order_id: int, feature_id: int) -> bool:
        link = await self.get_by_id(order_id, feature_id)
        if not link:
            return False
        await self.db.delete(link)
        await self.db.commit()
        return True


async def get_order_to_feature_service(
    db: AsyncSession = Depends(get_db),
) -> OrderToFeatureService:
    return OrderToFeatureService(db)
