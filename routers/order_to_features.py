import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.order_to_feature import OrderToFeature
from schemas.order_to_feature import OrderToFeatureCreate, OrderToFeatureRead
from settings.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/order-to-features", tags=["Order To Features"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[OrderToFeatureRead])
async def get_order_to_features(session: SessionDepend):
    try:
        result = await session.execute(select(OrderToFeature))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching order-to-feature links")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{order_id}/{feature_id}", response_model=OrderToFeatureRead)
async def get_order_to_feature(order_id: int, feature_id: int, session: SessionDepend):
    try:
        link = await session.get(OrderToFeature, (order_id, feature_id))
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order-to-feature link not found",
            )
        return link
    except HTTPException:
        raise
    except Exception:
        logger.exception(
            "Error fetching order-to-feature link %s/%s", order_id, feature_id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("", response_model=OrderToFeatureRead, status_code=status.HTTP_201_CREATED)
async def create_order_to_feature(data: OrderToFeatureCreate, session: SessionDepend):
    try:
        link = OrderToFeature(**data.model_dump())
        session.add(link)
        await session.flush()
        await session.refresh(link)
        return link
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating order-to-feature link")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete("/{order_id}/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_to_feature(
    order_id: int, feature_id: int, session: SessionDepend
):
    try:
        link = await session.get(OrderToFeature, (order_id, feature_id))
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order-to-feature link not found",
            )
        await session.delete(link)
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception(
            "Error deleting order-to-feature link %s/%s", order_id, feature_id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
