import uuid
from abc import ABC, abstractmethod

from app.schemas import UserInDB


class IUserRepository(ABC):
    @abstractmethod
    async def get_user_with_id(self, user_id: uuid.UUID) -> UserInDB | None:
        """Get user by ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_user_with_username(self, username: str) -> UserInDB | None:
        """Get user by username."""
        raise NotImplementedError

    @abstractmethod
    async def get_user_with_email(self, email: str) -> UserInDB | None:
        """Get user by email."""
        raise NotImplementedError

    @abstractmethod
    async def get_all_users(
        self, offset: int = 0, limit: int = 50, is_active: bool | None = None
    ) -> list[UserInDB]:
        """Get all users with optional filtering."""
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: UserInDB) -> UserInDB | None:
        """Create new user."""
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user_id: uuid.UUID, user: UserInDB) -> UserInDB | None:
        """Update user."""
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: uuid.UUID) -> bool:
        """Delete user (hard delete)."""
        raise NotImplementedError

    @abstractmethod
    async def soft_delete_user(self, user_id: uuid.UUID) -> UserInDB | None:
        """Soft delete user (set is_active=False, set deleted_at)."""
        raise NotImplementedError

    @abstractmethod
    async def restore_user(self, user_id: uuid.UUID) -> UserInDB | None:
        """Restore soft-deleted user (set is_active=True, clear deleted_at)."""
        raise NotImplementedError
