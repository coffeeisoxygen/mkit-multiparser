from fastapi import APIRouter, Depends, Request

from app.deps.dep_auth import get_auth_service, get_request_context
from app.deps.dep_security import get_is_active_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/login")
async def login(
    identifier: str,
    password: str,
    request: Request,
    auth_service=Depends(get_auth_service),
):
    context = get_request_context(request)
    result = await auth_service.authenticate_and_issue_token(
        identifier=identifier,
        password=password,
        ip_address=context["client_ip"],
        user_agent=context["user_agent"],
    )
    return result


@router.get("/profile")
async def profile(current_user=Depends(get_is_active_user)):
    """Endpoint untuk mengambil profile user yang sudah login dan aktif."""
    return current_user
