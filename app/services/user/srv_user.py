"""Service untuk user management."""

from typing import Any

from loguru import logger
from pydantic import ValidationError

from app.database.interfaces import IUserRepository
from app.exception import (
    UserCreationError,
    UserDuplicateError,
)
from app.schemas.user import UserCreate, UserPublicResponse
from app.utils.hasher.interface import HasherInterface


class UserService:
    """Service untuk register, login, dan integrasi session/token."""

    def __init__(
        self,
        user_repo: IUserRepository,
        hasher: HasherInterface,
    ):
        self.user_repo: IUserRepository = user_repo
        self.hasher: HasherInterface = hasher

    async def register_user(self, user_data: UserCreate) -> UserPublicResponse:
        """Register user baru (admin membuat user).

        Memastikan username dan email unik sebelum membuat user baru.
        """

        def _check_duplicate(existing_user: Any, existing_email: Any):
            """Raise exception jika username/email sudah digunakan."""
            if existing_user:
                raise UserDuplicateError("Username sudah digunakan.")
            if existing_email:
                raise UserDuplicateError("Email sudah digunakan.")

        try:
            # Cek apakah username atau email sudah ada
            existing_user = await self.user_repo.get_user_with_username(
                user_data.username
            )
            existing_email = await self.user_repo.get_user_with_email(user_data.email)
            _check_duplicate(existing_user, existing_email)

            # Hash password sebelum menyimpan
            hashed_password = self.hasher.hash(user_data.password)
            user_data.password = hashed_password

            # Buat user baru
            db_user = await self.user_repo.create(user_data.model_dump())
            if isinstance(db_user, UserPublicResponse):
                return db_user
            return UserPublicResponse.model_validate(db_user)

        except UserDuplicateError:
            # Biarkan bubble up, agar test bisa catch
            raise
        except ValidationError as e:
            logger.error(f"Validation error during user registration: {e}")
            raise UserCreationError("Data user tidak valid.") from e
        except Exception as e:
            logger.error(f"Unexpected error during user registration: {e}")
            raise UserCreationError("Gagal membuat user baru.") from e
