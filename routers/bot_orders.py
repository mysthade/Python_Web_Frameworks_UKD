import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.bot_order import BotOrder
from schemas.bot_order import BotOrderCreate, BotOrderRead, BotOrderUpdate
from settings.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bot-orders", tags=["Bot Orders"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[BotOrderRead])
async def get_bot_orders(session: SessionDepend):
    try:
        result = await session.execute(select(BotOrder))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching bot orders")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{order_id}", response_model=BotOrderRead)
async def get_bot_order(order_id: int, session: SessionDepend):
    try:
        order = await session.get(BotOrder, order_id)
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
async def create_bot_order(data: BotOrderCreate, session: SessionDepend):
    try:
        order = BotOrder(**data.model_dump())
        session.add(order)
        await session.flush()
        await session.refresh(order)
        return order
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating bot order")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/{order_id}", response_model=BotOrderRead)
async def update_bot_order(order_id: int, data: BotOrderUpdate, session: SessionDepend):
    try:
        order = await session.get(BotOrder, order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot order not found",
            )
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(order, key, value)
        await session.flush()
        await session.refresh(order)
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
async def delete_bot_order(order_id: int, session: SessionDepend):
    try:
        order = await session.get(BotOrder, order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot order not found",
            )
        await session.delete(order)
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting bot order %s", order_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
