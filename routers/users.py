from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from core.dependencies import require_access_token, require_admin
from core.handlers import run_handler
from schemas.user import UserCreate, UserRead, UserUpdate
from services.users import UserService, get_user_service
from utils.pdf import generate_users_report

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserRead])
async def get_users(user_service: UserService = Depends(get_user_service)):
    return await run_handler(
        lambda: user_service.get_all(),
        log_message="Error fetching users",
    )


@router.get("/report", summary="Generate users PDF report")
async def get_users_report(user_service: UserService = Depends(get_user_service)):
    async def handler():
        users = list(await user_service.get_all())
        report_path = generate_users_report(users)
        return FileResponse(
            path=report_path,
            media_type="application/pdf",
            filename=report_path.name,
        )

    return await run_handler(
        handler,
        log_message="Error generating users report",
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    async def handler():
        user = await user_service.get_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    return await run_handler(
        handler,
        log_message="Error fetching user %s",
        log_args=(user_id,),
    )


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    user_service: UserService = Depends(get_user_service),
    _: object = Depends(require_access_token),
):
    return await run_handler(
        lambda: user_service.create(data=data),
        log_message="Error creating user",
    )


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    async def handler():
        user = await user_service.update(user_id=user_id, data=data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    return await run_handler(
        handler,
        log_message="Error updating user %s",
        log_args=(user_id,),
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    _: object = Depends(require_admin),
):
    async def handler():
        deleted = await user_service.delete(user_id=user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return None

    return await run_handler(
        handler,
        log_message="Error deleting user %s",
        log_args=(user_id,),
    )
