"""router untuk admin / sys admin."""

from fastapi import APIRouter, Depends, Request

from app.config import get_settings
from app.custom.security.ip_filtering import IPFilter, ip_protected
from app.deps.dep_security import get_is_admin_user

router = APIRouter()


@router.get("/")
async def read_admin(current_admin=Depends(get_is_admin_user)):
    return {"message": "Hello Admin"}


@router.get("/debug")
async def debug_endpoint(current_admin=Depends(get_is_admin_user)):
    """Debug endpoint to dump all settings values.

    Returns:
        dict: All current settings values.
    """
    settings = get_settings()
    return {"settings": settings.model_dump()}


@router.get("/health")
@ip_protected(IPFilter(enabled=True))
async def health_check(request: Request):  # noqa: ARG001
    """Health check endpoint for admin router.

    Returns:
        dict: Status of the application.
    """
    return {"status": "healthy"}
