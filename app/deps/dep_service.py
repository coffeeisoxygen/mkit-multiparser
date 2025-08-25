"""Dependency factory untuk service (AuthService, UserService, dst).

Pisahkan dari repo agar lebih rapi dan maintainable.
"""

from fastapi import Depends

from app.deps.dep_factory import get_hasher, get_token_service
from app.deps.dep_repo import get_session_repo, get_user_repo
from app.services.session.srv_session import SessionService
from app.services.token.intf_token import ITokenService
from app.services.user.srv_auth import AuthService
from app.services.user.srv_user import UserService


async def get_auth_service(
    user_repo=Depends(get_user_repo),
    hasher=Depends(get_hasher),
    session_service: SessionService = Depends(),
    token_service: ITokenService = Depends(get_token_service),
) -> AuthService:
    """Dependency untuk inject AuthService."""
    return AuthService(user_repo, hasher, session_service, token_service)


async def get_user_service(
    user_repo=Depends(get_user_repo),
    hasher=Depends(get_hasher),
) -> UserService:
    """Dependency untuk inject UserService."""
    return UserService(user_repo, hasher)


async def get_session_service(
    session_repo=Depends(get_session_repo),
) -> SessionService:
    """Dependency untuk inject SessionService."""
    return SessionService(session_repo)


# Tambahkan factory service lain di sini jika diperlukan
