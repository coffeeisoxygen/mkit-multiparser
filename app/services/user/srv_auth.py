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
from app.schemas.user.sch_user import UserPublicResponse
from app.services.session.srv_session import SessionService
from app.services.token.intf_token import ITokenService
from app.utils.hasher.interface import HasherInterface


class AuthService:
    """Service untuk authentication dan authorization user."""

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

    async def login_user(self, username_or_email: str, password: str) -> dict:
        """Login user dengan username/email dan password.

        Args:
                username_or_email: Username atau email user.
                password: Password user (plain).

        Returns:
                Dict berisi user info, token, dan session info.
        """
        # Cari user by username/email
        user = await self.user_repo.get_user_with_username(username_or_email)
        if not user:
            user = await self.user_repo.get_user_with_email(username_or_email)
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

        # Generate session
        session_obj = await self.session_service.create_session(
            session_in={"user_id": user.id}
        )

        # Generate token
        token = self.token_service.create_token(
            user_id=user.id,
            is_superuser=user.is_superuser,
            is_active=user.is_active,
        )

        # Build response
        return {
            "user": UserPublicResponse.model_validate(user),
            "token": token,
            "session": session_obj,
        }
