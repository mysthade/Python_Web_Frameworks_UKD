import logging

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.bot_order import BotOrderCreate, BotOrderRead, BotOrderUpdate
from services.bot_orders import BotOrderService, get_bot_order_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bot-orders", tags=["Bot Orders"])


@router.get("", response_model=list[BotOrderRead])
async def get_bot_orders(
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    try:
        return await bot_order_service.get_all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching bot orders")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{order_id}", response_model=BotOrderRead)
async def get_bot_order(
    order_id: int,
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    try:
        order = await bot_order_service.get_by_id(order_id=order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot order not found",
            )
        return order
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching bot order %s", order_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("", response_model=BotOrderRead, status_code=status.HTTP_201_CREATED)
async def create_bot_order(
    data: BotOrderCreate,
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    try:
        return await bot_order_service.create(data=data)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating bot order")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/{order_id}", response_model=BotOrderRead)
async def update_bot_order(
    order_id: int,
    data: BotOrderUpdate,
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    try:
        order = await bot_order_service.update(order_id=order_id, data=data)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot order not found",
            )
        return order
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error updating bot order %s", order_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot_order(
    order_id: int,
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    try:
        deleted = await bot_order_service.delete(order_id=order_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot order not found",
            )
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting bot order %s", order_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
