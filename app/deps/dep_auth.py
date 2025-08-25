from fastapi import Depends, Request

from app.database.repositories.intf_user import IUserRepository
from app.services.session.srv_session import SessionService
from app.services.token.intf_token import ITokenService
from app.services.user.srv_auth import AuthService
from app.utils.hasher.interface import HasherInterface


def get_auth_service(
    user_repo: IUserRepository = Depends(),
    hasher: HasherInterface = Depends(),
    session_service: SessionService = Depends(),
    token_service: ITokenService = Depends(),
) -> AuthService:
    """Dependency untuk inject AuthService."""
    return AuthService(
        user_repo=user_repo,
        hasher=hasher,
        session_service=session_service,
        token_service=token_service,
    )


def get_request_context(request: Request) -> dict:
    """Ambil info kontekstual dari request (ip, user agent, headers)."""
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    return {
        "client_ip": client_ip,
        "user_agent": user_agent,
        "headers": dict(request.headers),
    }
