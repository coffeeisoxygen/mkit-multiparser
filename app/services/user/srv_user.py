"""Service untuk user management."""

from loguru import logger
from pydantic import ValidationError

from app.database.repositories.intf_user import IUserRepository
from app.exception import (
    UserCreationError,
    UserDuplicateError,
    UserPasswordGenericError,
)
from app.schemas.user.sch_user_crud import UserCreate, UserPublicResponse
from app.utils.hasher.interface import HasherInterface


class UserService:
    """Service untuk register, login, dan integrasi session/token."""

    def __init__(
        self,
        user_repo: IUserRepository,
        hasher: HasherInterface,
    ):
        self.user_repo = user_repo
        self.hasher = hasher

    async def register_user(self, user_data: UserCreate) -> UserPublicResponse:
        """Register user baru (admin membuat user).

        Memastikan username dan email unik sebelum membuat user baru.
        """
        try:
            user_data = UserCreate.model_validate(user_data)
        except ValidationError as ve:
            with logger.contextualize(username=getattr(user_data, "username", None)):
                logger.error("Password validation failed")
            raise UserPasswordGenericError(
                message="Password validation failed.",
                context={
                    "errors": ve.errors(),
                    "password": getattr(user_data, "password", None),
                },
                cause=ve,
            ) from ve

        with logger.contextualize(username=user_data.username, email=user_data.email):
            if await self.user_repo.get_user_with_username(user_data.username):
                logger.error("User already exists")
                raise UserDuplicateError(
                    f"Username {user_data.username} sudah terdaftar."
                )

            if await self.user_repo.get_user_with_email(user_data.email):
                logger.error("Email already exists")
                raise UserDuplicateError(f"Email {user_data.email} sudah terdaftar.")

            user_data.password = self.hasher.hash(user_data.password)
            new_user = await self.user_repo.create_user(user_data)
            if not new_user:
                logger.error("Failed to create user")
                raise UserCreationError(
                    message="Terjadi kesalahan saat membuat akun baru.",
                    context={"username": user_data.username},
                )
            return UserPublicResponse.model_validate(new_user)
