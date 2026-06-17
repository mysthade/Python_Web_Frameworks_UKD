from authx import RequestToken
from fastapi import Depends, HTTPException, status

from models.user import User, UserRole
from services.users import UserService, get_user_service
from utils.security import security


async def require_access_token(
    token: RequestToken = Depends(security.access_token_required),
) -> RequestToken:
    security.verify_token(token)
    return token


async def require_admin(
    token: RequestToken = Depends(security.access_token_required),
    user_service: UserService = Depends(get_user_service),
) -> User:
    payload = security.verify_token(token)
    current_user = await user_service.get_by_id(user_id=int(payload.sub))
    if not current_user or current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return current_user
