import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.bot_feature import BotFeature
from schemas.bot_feature import BotFeatureCreate, BotFeatureRead, BotFeatureUpdate
from settings.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bot-features", tags=["Bot Features"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[BotFeatureRead])
async def get_bot_features(session: SessionDepend):
    try:
        result = await session.execute(select(BotFeature))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching bot features")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{feature_id}", response_model=BotFeatureRead)
async def get_bot_feature(feature_id: int, session: SessionDepend):
    try:
        feature = await session.get(BotFeature, feature_id)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot feature not found",
            )
        return feature
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching bot feature %s", feature_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("", response_model=BotFeatureRead, status_code=status.HTTP_201_CREATED)
async def create_bot_feature(data: BotFeatureCreate, session: SessionDepend):
    try:
        feature = BotFeature(**data.model_dump())
        session.add(feature)
        await session.flush()
        await session.refresh(feature)
        return feature
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating bot feature")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/{feature_id}", response_model=BotFeatureRead)
async def update_bot_feature(
    feature_id: int, data: BotFeatureUpdate, session: SessionDepend
):
    try:
        feature = await session.get(BotFeature, feature_id)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot feature not found",
            )
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(feature, key, value)
        await session.flush()
        await session.refresh(feature)
        return feature
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error updating bot feature %s", feature_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot_feature(feature_id: int, session: SessionDepend):
    try:
        feature = await session.get(BotFeature, feature_id)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot feature not found",
            )
        await session.delete(feature)
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting bot feature %s", feature_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
