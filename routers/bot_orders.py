from fastapi import APIRouter, Depends, HTTPException, status

from core.handlers import run_handler
from schemas.bot_order import BotOrderCreate, BotOrderRead, BotOrderUpdate
from services.bot_orders import BotOrderService, get_bot_order_service

router = APIRouter(prefix="/bot-orders", tags=["Bot Orders"])


@router.get("", response_model=list[BotOrderRead])
async def get_bot_orders(
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    return await run_handler(
        lambda: bot_order_service.get_all(),
        log_message="Error fetching bot orders",
    )


@router.get("/{order_id}", response_model=BotOrderRead)
async def get_bot_order(
    order_id: int,
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    async def handler():
        order = await bot_order_service.get_by_id(order_id=order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot order not found",
            )
        return order

    return await run_handler(
        handler,
        log_message="Error fetching bot order %s",
        log_args=(order_id,),
    )


@router.post("", response_model=BotOrderRead, status_code=status.HTTP_201_CREATED)
async def create_bot_order(
    data: BotOrderCreate,
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    return await run_handler(
        lambda: bot_order_service.create(data=data),
        log_message="Error creating bot order",
    )


@router.patch("/{order_id}", response_model=BotOrderRead)
async def update_bot_order(
    order_id: int,
    data: BotOrderUpdate,
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    async def handler():
        order = await bot_order_service.update(order_id=order_id, data=data)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot order not found",
            )
        return order

    return await run_handler(
        handler,
        log_message="Error updating bot order %s",
        log_args=(order_id,),
    )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot_order(
    order_id: int,
    bot_order_service: BotOrderService = Depends(get_bot_order_service),
):
    async def handler():
        deleted = await bot_order_service.delete(order_id=order_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot order not found",
            )
        return None

    return await run_handler(
        handler,
        log_message="Error deleting bot order %s",
        log_args=(order_id,),
    )
