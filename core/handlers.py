import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def run_handler(
    handler: Callable[[], Awaitable[T]],
    *,
    log_message: str,
    log_args: tuple = (),
    error_detail: str = "Internal server error",
) -> T:
    try:
        return await handler()
    except HTTPException:
        raise
    except Exception:
        logger.exception(log_message, *log_args)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail,
        )
