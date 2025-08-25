"""Database user repository interface definitions.

This module defines the IUserRepository protocol, which specifies
the contract for user-related database operations. Implementations
should provide asynchronous methods for CRUD and user management.
"""

# ...existing code...
from typing import Protocol

from app.models.db_user import User
from app.schemas.user.sch_user import UserCreate, UserUpdate


class IUserRepository(Protocol):
    """Protocol for user repository operations.

    This interface defines asynchronous methods for retrieving,
    creating, updating, deleting, and restoring user records.
    """

    async def get_user_with_id(self, user_id: str) -> User | None:
        """Retrieve a user by their unique ID.

        Args:
            user_id: The string UUID of the user.

        Returns:
            The User object if found, otherwise None.
        """
        ...

    async def get_user_with_username(self, username: str) -> User | None:
        """Retrieve a user by their username.

        Args:
            username: The username of the user.

        Returns:
            The User object if found, otherwise None.
        """
        ...

    async def get_user_with_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email: The email address of the user.

        Returns:
            The User object if found, otherwise None.
        """
        ...

    async def get_all_users(
        self, offset: int = 0, limit: int = 50, is_active: bool | None = None
    ) -> list[User]:
        """Retrieve all users with optional pagination and active status filter.

        Args:
            offset: The starting index for pagination.
            limit: The maximum number of users to return.
            is_active: Optional filter for active users.

        Returns:
            A list of User objects.
        """
        ...

    async def create_user(self, user_in: UserCreate) -> User:
        """Create a new user record.

        Args:
            user_in: The data required to create a user.

        Returns:
            The created User object.
        """
        ...

    async def update_user(self, user_id: str, user_in: UserUpdate) -> User | None:
        """Update an existing user record.

        Args:
            user_id: The string UUID of the user to update.
            user_in: The updated user data.

        Returns:
            The updated User object if found, otherwise None.
        """
        ...

    async def delete_user(self, user_id: str) -> bool:
        """Permanently delete a user record.

        Args:
            user_id: The string UUID of the user to delete.

        Returns:
            True if deletion was successful, False otherwise.
        """
        ...

    async def soft_delete_user(self, user_id: str) -> User | None:
        """Soft delete a user (mark as inactive or deleted).

        Args:
            user_id: The string UUID of the user to soft delete.

        Returns:
            The updated User object if found, otherwise None.
        """
        ...

    async def restore_user(self, user_id: str) -> User | None:
        """Restore a previously soft-deleted user.

        Args:
            user_id: The string UUID of the user to restore.

        Returns:
            The restored User object if found, otherwise None.
        """
        ...

    async def activate_user(self, user_id: str) -> User | None:
        """Activate a user account.

        Args:
            user_id: The string UUID of the user to activate.

        Returns:
            The updated User object if found, otherwise None.
        """
        ...

    async def deactivate_user(self, user_id: str) -> User | None:
        """Deactivate a user account.

        Args:
            user_id: The string UUID of the user to deactivate.

        Returns:
            The updated User object if found, otherwise None.
        """
        ...
