"""Service untuk authentication dan authorization user.

Fitur utama:
        - Login user (username/email + password)
        - Generate session dan token
        - Validasi password
        - Response: user info + token + session info
"""

from loguru import logger

from app.database.repositories.intf_user import IUserRepository
from app.exception import (
    UserInActiveError,
    UserNotFoundError,
    UserPasswordGenericError,
)
from app.schemas.user import UserLoginResponse, UserPublicResponse
from app.schemas.user.sch_user_session import SessionCreate
from app.schemas.user.sch_user_token import TokenResponse
from app.services.session.srv_session import SessionService
from app.services.token.intf_token import ITokenService
from app.utils.hasher.interface import HasherInterface


class AuthService:
    """Service untuk authentication dan token generation.

    - Validasi user dan password
    - Generate JWT token (sub=username)
    - Buat session dengan user_id, ip_address, user_agent
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        hasher: HasherInterface,
        session_service: SessionService,
        token_service: ITokenService,
    ):
        self.user_repo = user_repo
        self.hasher = hasher
        self.session_service = session_service
        self.token_service = token_service

    async def auth_user(self, identifier: str, password: str):
        """Validasi user dan password, return user object jika valid."""
        user = await self.user_repo.get_user_with_username(identifier)
        if not user:
            user = await self.user_repo.get_user_with_email(identifier)
        if not user:
            logger.error("User not found for login")
            raise UserNotFoundError("User tidak ditemukan.")

        if not user.is_active:
            logger.error("User inactive for login")
            raise UserInActiveError("User tidak aktif.")

        if not self.hasher.verify(password, user.hashed_password):
            logger.error("Password invalid for login")
            raise UserPasswordGenericError("Password salah.")
        return user

    def create_token(self, user) -> TokenResponse:
        """Generate JWT token dari user object dan bungkus ke TokenResponse."""
        token_str = self.token_service.create_token(
            user_id=user.id,
            username=user.username,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
        )
        # expires_in diambil dari config token_service
        return TokenResponse(
            access_token=token_str,
            expires_in=getattr(self.token_service, "expire_minutes", 60),
        )

    async def create_session(
        self, user, ip_address: str | None = None, user_agent: str | None = None
    ):
        """Buat session dari user object dan info request."""
        return await self.session_service.create_session(
            session_in=SessionCreate(
                user_id=user.id,
                token="",  # token session bisa diisi jika ada
                ip_address=ip_address or "",
                user_agent=user_agent or "",
            )
        )

    async def authenticate_and_issue_token(
        self,
        identifier: str,
        password: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> dict:
        """Orkestrasi: auth, session, token, build response."""
        user = await self.auth_user(identifier, password)
        session_obj = await self.create_session(user, ip_address, user_agent)
        token = self.create_token(user)
        return {
            "user": UserPublicResponse.model_validate(user),
            "token": token,
            "session": UserLoginResponse.model_validate(session_obj),
        }
