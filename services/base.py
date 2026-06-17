from collections.abc import Callable
from typing import ClassVar, Generic, TypeVar

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from settings.db import get_db

ModelT = TypeVar("ModelT", bound=DeclarativeBase)
CreateT = TypeVar("CreateT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)
ServiceT = TypeVar("ServiceT")


class BaseCRUDService(Generic[ModelT, CreateT, UpdateT]):
    model: ClassVar[type[ModelT]]

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, entity_id: int) -> ModelT | None:
        return await self.db.get(self.model, entity_id)

    async def create(self, data: CreateT) -> ModelT:
        entity = self.model(**data.model_dump())
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def update(self, entity_id: int, data: UpdateT) -> ModelT | None:
        entity = await self.get_by_id(entity_id)
        if not entity:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(entity, key, value)
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity_id: int) -> bool:
        entity = await self.get_by_id(entity_id)
        if not entity:
            return False
        await self.db.delete(entity)
        await self.db.commit()
        return True


def service_dependency(service_cls: type[ServiceT]) -> Callable[..., ServiceT]:
    async def _get_service(db: AsyncSession = Depends(get_db)) -> ServiceT:
        return service_cls(db)

    return _get_service
