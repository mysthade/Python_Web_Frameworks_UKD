from fastapi import APIRouter, Depends, HTTPException, status

from core.handlers import run_handler
from schemas.bot_feature import BotFeatureCreate, BotFeatureRead, BotFeatureUpdate
from services.bot_features import BotFeatureService, get_bot_feature_service

router = APIRouter(prefix="/bot-features", tags=["Bot Features"])


@router.get("", response_model=list[BotFeatureRead])
async def get_bot_features(
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    return await run_handler(
        lambda: bot_feature_service.get_all(),
        log_message="Error fetching bot features",
    )


@router.get("/{feature_id}", response_model=BotFeatureRead)
async def get_bot_feature(
    feature_id: int,
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    async def handler():
        feature = await bot_feature_service.get_by_id(feature_id=feature_id)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot feature not found",
            )
        return feature

    return await run_handler(
        handler,
        log_message="Error fetching bot feature %s",
        log_args=(feature_id,),
    )


@router.post("", response_model=BotFeatureRead, status_code=status.HTTP_201_CREATED)
async def create_bot_feature(
    data: BotFeatureCreate,
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    return await run_handler(
        lambda: bot_feature_service.create(data=data),
        log_message="Error creating bot feature",
    )


@router.patch("/{feature_id}", response_model=BotFeatureRead)
async def update_bot_feature(
    feature_id: int,
    data: BotFeatureUpdate,
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    async def handler():
        feature = await bot_feature_service.update(feature_id=feature_id, data=data)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot feature not found",
            )
        return feature

    return await run_handler(
        handler,
        log_message="Error updating bot feature %s",
        log_args=(feature_id,),
    )


@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot_feature(
    feature_id: int,
    bot_feature_service: BotFeatureService = Depends(get_bot_feature_service),
):
    async def handler():
        deleted = await bot_feature_service.delete(feature_id=feature_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot feature not found",
            )
        return None

    return await run_handler(
        handler,
        log_message="Error deleting bot feature %s",
        log_args=(feature_id,),
    )
