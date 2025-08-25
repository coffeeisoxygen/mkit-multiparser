"""Service untuk user authentication: register, login, dan integrasi session/token."""

from loguru import logger

from app.database.repositories.intf_user import IUserRepository
from app.exception import (
    UserCreationError,
    UserDuplicateError,
)
from app.schemas.user.sch_user import UserCreate, UserPublicResponse
from app.services.session.srv_session import SessionService
from app.services.token.intf_token import ITokenService
from app.utils.hasher.interface import HasherInterface


class UserAuthService:
    """Service untuk register, login, dan integrasi session/token."""

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

    async def register_user(self, user_data: UserCreate) -> UserPublicResponse:
        """Register user baru (admin membuat user)."""
        existing_user = await self.user_repo.get_user_with_username(user_data.username)
        if existing_user:
            logger.bind(username=user_data.username).error("User already exists")
            raise UserDuplicateError(f"Username {user_data.username} sudah terdaftar.")
        hashed_password = self.hasher.hash(user_data.password)
        user_data.password = hashed_password
        new_user = await self.user_repo.create_user(user_data)
        if not new_user:
            logger.bind(username=user_data.username).error("Failed to create user")
            raise UserCreationError("Terjadi kesalahan saat membuat akun baru.")
        return UserPublicResponse.model_validate(new_user)
