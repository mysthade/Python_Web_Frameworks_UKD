from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.profile import Profile
from schemas.profile import ProfileCreate, ProfileUpdate
from settings.db import get_db


class ProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[Profile]:
        result = await self.db.execute(select(Profile))
        return result.scalars().all()

    async def get_by_id(self, profile_id: int) -> Profile | None:
        return await self.db.get(Profile, profile_id)

    async def create(self, data: ProfileCreate) -> Profile:
        profile = Profile(**data.model_dump())
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def update(self, profile_id: int, data: ProfileUpdate) -> Profile | None:
        profile = await self.get_by_id(profile_id)
        if not profile:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def delete(self, profile_id: int) -> bool:
        profile = await self.get_by_id(profile_id)
        if not profile:
            return False
        await self.db.delete(profile)
        await self.db.commit()
        return True


async def get_profile_service(db: AsyncSession = Depends(get_db)) -> ProfileService:
    return ProfileService(db)
