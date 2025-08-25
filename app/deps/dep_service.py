"""Dependency factory untuk service (AuthService, UserService, dst).

Pisahkan dari repo agar lebih rapi dan maintainable.
"""

from fastapi import Depends

from app.config import get_settings
from app.deps.dep_repo import get_session_repo, get_user_repo
from app.deps.dep_utils import get_hasher
from app.services.session.srv_session import SessionService
from app.services.token.intf_token import ITokenService
from app.services.token.srv_token import TokenService
from app.services.user.srv_auth import AuthService
from app.services.user.srv_user import UserService


def get_auth_service(
    user_repo=Depends(get_user_repo),
    hasher=Depends(get_hasher),
    session_service: SessionService = Depends(),
    token_service: ITokenService = Depends(),
) -> AuthService:
    """Dependency untuk inject AuthService."""
    return AuthService(user_repo, hasher, session_service, token_service)


def get_user_service(
    user_repo=Depends(get_user_repo),
    hasher=Depends(get_hasher),
) -> UserService:
    """Dependency untuk inject UserService."""
    return UserService(user_repo, hasher)


def get_session_service(
    session_repo=Depends(get_session_repo),
) -> SessionService:
    """Dependency untuk inject SessionService."""
    return SessionService(session_repo)


def get_token_service(
    settings=Depends(get_settings),
) -> TokenService:
    """Dependency untuk inject TokenService.

    Args:
        settings: Konfigurasi aplikasi.

    Returns:
        TokenService: Instance TokenService dengan konfigurasi dari settings.
    """
    return TokenService(
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        expire_minutes=settings.JWT_EXPIRE_MINUTES,
    )
