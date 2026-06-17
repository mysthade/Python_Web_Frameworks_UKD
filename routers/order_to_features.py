from fastapi import APIRouter, Depends, HTTPException, status

from core.handlers import run_handler
from schemas.order_to_feature import OrderToFeatureCreate, OrderToFeatureRead
from services.order_to_features import (
    OrderToFeatureService,
    get_order_to_feature_service,
)

router = APIRouter(prefix="/order-to-features", tags=["Order To Features"])


@router.get("", response_model=list[OrderToFeatureRead])
async def get_order_to_features(
    order_to_feature_service: OrderToFeatureService = Depends(
        get_order_to_feature_service
    ),
):
    return await run_handler(
        lambda: order_to_feature_service.get_all(),
        log_message="Error fetching order-to-feature links",
    )


@router.get("/{order_id}/{feature_id}", response_model=OrderToFeatureRead)
async def get_order_to_feature(
    order_id: int,
    feature_id: int,
    order_to_feature_service: OrderToFeatureService = Depends(
        get_order_to_feature_service
    ),
):
    async def handler():
        link = await order_to_feature_service.get_by_id(order_id, feature_id)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order-to-feature link not found",
            )
        return link

    return await run_handler(
        handler,
        log_message="Error fetching order-to-feature link %s/%s",
        log_args=(order_id, feature_id),
    )


@router.post("", response_model=OrderToFeatureRead, status_code=status.HTTP_201_CREATED)
async def create_order_to_feature(
    data: OrderToFeatureCreate,
    order_to_feature_service: OrderToFeatureService = Depends(
        get_order_to_feature_service
    ),
):
    return await run_handler(
        lambda: order_to_feature_service.create(data=data),
        log_message="Error creating order-to-feature link",
    )


@router.delete("/{order_id}/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_to_feature(
    order_id: int,
    feature_id: int,
    order_to_feature_service: OrderToFeatureService = Depends(
        get_order_to_feature_service
    ),
):
    async def handler():
        deleted = await order_to_feature_service.delete(order_id, feature_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order-to-feature link not found",
            )
        return None

    return await run_handler(
        handler,
        log_message="Error deleting order-to-feature link %s/%s",
        log_args=(order_id, feature_id),
    )
