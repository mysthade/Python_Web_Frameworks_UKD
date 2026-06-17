from fastapi import APIRouter, Depends, HTTPException, status

from core.handlers import run_handler
from schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate
from services.profiles import ProfileService, get_profile_service

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("", response_model=list[ProfileRead])
async def get_profiles(profile_service: ProfileService = Depends(get_profile_service)):
    return await run_handler(
        lambda: profile_service.get_all(),
        log_message="Error fetching profiles",
    )


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile(
    profile_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
):
    async def handler():
        profile = await profile_service.get_by_id(profile_id=profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
        return profile

    return await run_handler(
        handler,
        log_message="Error fetching profile %s",
        log_args=(profile_id,),
    )


@router.post("", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(
    data: ProfileCreate,
    profile_service: ProfileService = Depends(get_profile_service),
):
    return await run_handler(
        lambda: profile_service.create(data=data),
        log_message="Error creating profile",
    )


@router.patch("/{profile_id}", response_model=ProfileRead)
async def update_profile(
    profile_id: int,
    data: ProfileUpdate,
    profile_service: ProfileService = Depends(get_profile_service),
):
    async def handler():
        profile = await profile_service.update(profile_id=profile_id, data=data)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
        return profile

    return await run_handler(
        handler,
        log_message="Error updating profile %s",
        log_args=(profile_id,),
    )


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    profile_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
):
    async def handler():
        deleted = await profile_service.delete(profile_id=profile_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
        return None

    return await run_handler(
        handler,
        log_message="Error deleting profile %s",
        log_args=(profile_id,),
    )
