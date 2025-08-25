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

    async def authenticate_and_issue_token(
        self,
        identifier: str,
        password: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> dict:
        """Authenticate user and issue JWT token + session.

        Args:
            identifier: Username atau email user.
            password: Password user (plain).
            ip_address: IP address dari request (opsional).
            user_agent: User agent dari request (opsional).

        Returns:
            Dict berisi user info, token, dan session.
        """
        user = await self.user_repo.get_user_with_username(identifier)
        if not user:
            user = await self.user_repo.get_user_with_email(identifier)
        if not user:
            logger.error("User not found for login")
            raise UserNotFoundError("User tidak ditemukan.")

        if not user.is_active:
            logger.error("User inactive for login")
            raise UserInActiveError("User tidak aktif.")

        # Validasi password
        if not self.hasher.verify(password, user.hashed_password):
            logger.error("Password invalid for login")
            raise UserPasswordGenericError("Password salah.")

        # Buat session dengan user_id, ip_address, user_agent

        session_obj = await self.session_service.create_session(
            session_in=SessionCreate(
                user_id=user.id,
                token="",  # token session bisa diisi jika ada
                ip_address=ip_address or "",
                user_agent=user_agent or "",
            )
        )

        # Generate token (sub=username)
        token = self.token_service.create_token(
            user_id=user.id,
            username=user.username,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
        )

        # Build response
        return {
            "user": UserPublicResponse.model_validate(user),
            "token": token,
            "session": UserLoginResponse.model_validate(session_obj),
        }
