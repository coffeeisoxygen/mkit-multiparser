import uuid
from abc import ABC, abstractmethod

from app.schemas.user.sch_user import (
    UserCreate,
    UserInDB,
    UserUpdate,
)


class IUserRepository(ABC):
    @abstractmethod
    async def get_user_with_id(self, user_id: uuid.UUID) -> UserInDB | None:
        """Get a user by their ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_user_with_username(self, username: str) -> UserInDB | None:
        """Get a user by their username."""
        raise NotImplementedError

    @abstractmethod
    async def get_user_with_email(self, email: str) -> UserInDB | None:
        """Get a user by their email."""
        raise NotImplementedError

    @abstractmethod
    async def get_all_users(
        self, offset: int = 0, limit: int = 50, is_active: bool | None = None
    ) -> list[UserInDB]:
        """Get all users with optional filtering."""
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user_in: UserCreate) -> UserInDB:
        """Create a new user from a UserCreate schema."""
        raise NotImplementedError

    @abstractmethod
    async def update_user(
        self, user_id: uuid.UUID, user_in: UserUpdate
    ) -> UserInDB | None:
        """Update a user from a UserUpdate schema."""
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: uuid.UUID) -> bool:
        """Permanently delete a user from the database."""
        raise NotImplementedError

    @abstractmethod
    async def soft_delete_user(self, user_id: uuid.UUID) -> UserInDB | None:
        """Soft delete a user by deactivating them and setting a deletion timestamp."""
        raise NotImplementedError

    @abstractmethod
    async def restore_user(self, user_id: uuid.UUID) -> UserInDB | None:
        """Restore a soft-deleted user."""
        raise NotImplementedError
