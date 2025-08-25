# ruff: noqa
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database.core.session import get_db_session_manual_commit, get_db_transaction
from app.database.repositories.intf_session import ISessionRepository
from app.database.repositories.intf_user import IUserRepository
from app.database.repositories.repo_session import SessionRepository
from app.database.repositories.repo_user import UserRepository
from app.services.session.srv_session import SessionService
from app.services.token.intf_token import ITokenService
from app.services.token.srv_token import TokenService
from app.services.user.srv_auth import AuthService, HasherInterface
from app.utils.hasher.argon_hasher import Argon2Hasher


async def get_session():
    """Dependency FastAPI untuk mendapatkan session database dengan Unit of Work pattern.

    Yields:
        AsyncSession: Session database yang siap digunakan untuk operasi ORM.
    """
    async with get_db_transaction() as session:
        yield session


async def get_session_manual():
    """Dependency FastAPI untuk mendapatkan session database dengan kontrol manual commit.

    Yields:
        AsyncSession: Session database yang membutuhkan commit/rollback manual.
    """
    async with get_db_session_manual_commit() as session:
        yield session


# here for all repositories.. adjust and add later
async def get_user_repo(
    session: AsyncSession = Depends(get_session),
) -> IUserRepository:
    return UserRepository(session)


async def get_session_repo(
    session: AsyncSession = Depends(get_session),
) -> ISessionRepository:
    return SessionRepository(session)


# here for all services...adjust and add ...
async def get_token_service() -> ITokenService:
    """Dependency FastAPI untuk mendapatkan TokenService.

    Returns:
        ITokenService: Instance dari TokenService.
    """
    settings = get_settings()
    return TokenService(
        secret_key=settings.JWT.SECRET_KEY,
        algorithm=settings.JWT.ALGORITHM,
        expire_minutes=settings.JWT.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


async def get_session_service(
    session_repo: ISessionRepository = Depends(get_session_repo),
) -> SessionService:
    """Dependency FastAPI untuk mendapatkan SessionService.

    Args:
        session_repo (ISessionRepository): Repository session.

    Returns:
        SessionService: Instance dari SessionService.
    """
    return SessionService(session_repo)


async def get_hasher() -> HasherInterface:
    return Argon2Hasher()


async def get_auth_service(
    user_repo: IUserRepository = Depends(get_user_repo),
    hasher: HasherInterface = Depends(get_hasher),
    session_service: SessionService = Depends(get_session_service),
    token_service: ITokenService = Depends(get_token_service),
) -> AuthService:
    return AuthService(user_repo, hasher, session_service, token_service)
