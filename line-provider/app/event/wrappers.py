from fastapi import HTTPException, status
from functools import wraps

from app.event.exception import EventNotFoundException


def handle_raisers(func):
    """Checker-Wrapper: raiser HTTPException to events"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except EventNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.detail
            )
    return wrapper
