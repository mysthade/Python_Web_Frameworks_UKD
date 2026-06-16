import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate
from settings.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[UserRead])
async def get_users(session: SessionDepend):
    try:
        result = await session.execute(select(User))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching users")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: SessionDepend):
    try:
        user = await session.get(User, user_id)
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
async def create_user(data: UserCreate, session: SessionDepend):
    try:
        user = User(**data.model_dump())
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, data: UserUpdate, session: SessionDepend):
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await session.flush()
        await session.refresh(user)
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
async def delete_user(user_id: int, session: SessionDepend):
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        await session.delete(user)
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting user %s", user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
