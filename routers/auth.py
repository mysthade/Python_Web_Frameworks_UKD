from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from core.handlers import run_handler
from schemas.auth import RegisterRequest
from schemas.user import UserRead
from services.auth import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await run_handler(
        lambda: auth_service.register(payload),
        log_message="Registration failed",
        error_detail="Registration failed",
    )


@router.post("/login")
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await run_handler(
        lambda: auth_service.login(credentials.username, credentials.password),
        log_message="Login failed",
        error_detail="Login failed",
    )
