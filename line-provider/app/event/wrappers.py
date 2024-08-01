from fastapi import HTTPException, status
from functools import wraps

from app.event.exception import EventNotFoundException


def not_found_handle(func):
    """Checker-Wrapper: raise HTTPException 404 status  to undefined event"""

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
