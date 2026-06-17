from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.bot_feature import BotFeature
from schemas.bot_feature import BotFeatureCreate, BotFeatureUpdate
from settings.db import get_db


class BotFeatureService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[BotFeature]:
        result = await self.db.execute(select(BotFeature))
        return result.scalars().all()

    async def get_by_id(self, feature_id: int) -> BotFeature | None:
        return await self.db.get(BotFeature, feature_id)

    async def create(self, data: BotFeatureCreate) -> BotFeature:
        feature = BotFeature(**data.model_dump())
        self.db.add(feature)
        await self.db.commit()
        await self.db.refresh(feature)
        return feature

    async def update(
        self, feature_id: int, data: BotFeatureUpdate
    ) -> BotFeature | None:
        feature = await self.get_by_id(feature_id)
        if not feature:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(feature, key, value)
        self.db.add(feature)
        await self.db.commit()
        await self.db.refresh(feature)
        return feature

    async def delete(self, feature_id: int) -> bool:
        feature = await self.get_by_id(feature_id)
        if not feature:
            return False
        await self.db.delete(feature)
        await self.db.commit()
        return True


async def get_bot_feature_service(
    db: AsyncSession = Depends(get_db),
) -> BotFeatureService:
    return BotFeatureService(db)
