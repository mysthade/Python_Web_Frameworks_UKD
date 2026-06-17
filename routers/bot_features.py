import logging

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.bot_feature import BotFeatureCreate, BotFeatureRead, BotFeatureUpdate
from services.bot_features import BotFeatureService, get_bot_feature_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bot-features", tags=["Bot Features"])


@router.get("", response_model=list[BotFeatureRead])
async def get_bot_features(
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    try:
        return await bot_feature_service.get_all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching bot features")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{feature_id}", response_model=BotFeatureRead)
async def get_bot_feature(
    feature_id: int,
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    try:
        feature = await bot_feature_service.get_by_id(feature_id=feature_id)
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
async def create_bot_feature(
    data: BotFeatureCreate,
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    try:
        return await bot_feature_service.create(data=data)
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
    feature_id: int,
    data: BotFeatureUpdate,
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    try:
        feature = await bot_feature_service.update(feature_id=feature_id, data=data)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot feature not found",
            )
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
async def delete_bot_feature(
    feature_id: int,
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    try:
        deleted = await bot_feature_service.delete(feature_id=feature_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot feature not found",
            )
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting bot feature %s", feature_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
