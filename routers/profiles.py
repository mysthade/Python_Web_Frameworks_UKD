import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.profile import Profile
from schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate
from settings.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profiles", tags=["Profiles"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[ProfileRead])
async def get_profiles(session: SessionDepend):
    try:
        result = await session.execute(select(Profile))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching profiles")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile(profile_id: int, session: SessionDepend):
    try:
        profile = await session.get(Profile, profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
        return profile
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching profile %s", profile_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(data: ProfileCreate, session: SessionDepend):
    try:
        profile = Profile(**data.model_dump())
        session.add(profile)
        await session.flush()
        await session.refresh(profile)
        return profile
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating profile")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/{profile_id}", response_model=ProfileRead)
async def update_profile(profile_id: int, data: ProfileUpdate, session: SessionDepend):
    try:
        profile = await session.get(Profile, profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)
        await session.flush()
        await session.refresh(profile)
        return profile
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error updating profile %s", profile_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(profile_id: int, session: SessionDepend):
    try:
        profile = await session.get(Profile, profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
        await session.delete(profile)
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting profile %s", profile_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
