import logging

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.user import UserCreate, UserRead, UserUpdate
from services.users import UserService, get_user_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserRead])
async def get_users(user_service: UserService = Depends(get_user_service)):
    try:
        return await user_service.get_all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching users")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        user = await user_service.get_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching user %s", user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.create(data=data)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = await user_service.update(user_id=user_id, data=data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error updating user %s", user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    try:
        deleted = await user_service.delete(user_id=user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting user %s", user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
