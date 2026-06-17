import logging

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate
from services.profiles import ProfileService, get_profile_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("", response_model=list[ProfileRead])
async def get_profiles(profile_service: ProfileService = Depends(get_profile_service)):
    try:
        return await profile_service.get_all()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error fetching profiles")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile(
    profile_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
):
    try:
        profile = await profile_service.get_by_id(profile_id=profile_id)
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
async def create_profile(
    data: ProfileCreate, profile_service: ProfileService = Depends(get_profile_service)
):
    try:
        return await profile_service.create(data=data)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error creating profile")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.patch("/{profile_id}", response_model=ProfileRead)
async def update_profile(
    profile_id: int,
    data: ProfileUpdate,
    profile_service: ProfileService = Depends(get_profile_service),
):
    try:
        profile = await profile_service.update(profile_id=profile_id, data=data)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
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
async def delete_profile(
    profile_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
):
    try:
        deleted = await profile_service.delete(profile_id=profile_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
        return None
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error deleting profile %s", profile_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
