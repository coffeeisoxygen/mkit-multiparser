"""Database user repository interface definitions.

This module defines the IUserRepository protocol, which specifies
the contract for user-related database operations.

Implementations should provide asynchronous methods for CRUD,
user management, and administrative operations.

Typical usage involves dependency injection of a concrete
repository class implementing this protocol.
"""

from typing import Protocol

from app.models.db_user import User
from app.schemas.user.sch_user import UserCreate, UserUpdate


class IUserRepository(Protocol):
    """Protocol for user repository operations.

    This interface defines asynchronous methods for user management,
    including CRUD operations, status/lifecycle management, password
    changes, superuser administration, and user filtering/counting.

    Implementations should provide concrete logic for each method,
    typically interacting with a database backend.

    Usage:
        - Dependency injection for repository implementations.
        - Enables testability and loose coupling in business logic.

    Methods:
        create_user: Create a new user.
        get_user_with_id: Retrieve a user by ID (int).
        get_user_with_username: Retrieve a user by username.
        get_user_with_email: Retrieve a user by email.
        get_all_users: List users with optional filters.
        update_user: Update user details.
        delete_user: Permanently delete a user.
        soft_delete_user: Soft-delete a user.
        restore_user: Restore a soft-deleted user.
        activate_user: Activate a user account.
        deactivate_user: Deactivate a user account.
        change_password: Change a user's password.
        set_superuser: Grant superuser privileges.
        unset_superuser: Revoke superuser privileges.
        get_superusers: List superusers.
        get_soft_deleted_users: List soft-deleted users.
        get_users_by_filter: Filter users by criteria.
        count_users: Count users with optional filters.
    """

    # CRUD
    async def create_user(self, user_in: UserCreate) -> User: ...

    async def get_user_with_id(self, user_id: int) -> User | None: ...

    async def get_user_with_username(self, username: str) -> User | None: ...

    async def get_user_with_email(self, email: str) -> User | None: ...

    async def get_all_users(
        self, offset: int = 0, limit: int = 50, is_active: bool | None = None
    ) -> list[User]: ...

    async def update_user(self, user_id: int, user_in: UserUpdate) -> User | None: ...

    async def delete_user(self, user_id: int) -> bool: ...

    # Status & lifecycle
    async def soft_delete_user(self, user_id: int) -> User | None: ...

    async def restore_user(self, user_id: int) -> User | None: ...

    async def activate_user(self, user_id: int) -> User | None: ...

    async def deactivate_user(self, user_id: int) -> User | None: ...

    # Password
    async def change_password(self, user_id: int, new_password: str) -> bool: ...

    # Admin & superuser
    async def set_superuser(self, user_id: int) -> User | None: ...

    async def unset_superuser(self, user_id: int) -> User | None: ...

    async def get_superusers(self, offset: int = 0, limit: int = 50) -> list[User]: ...

    # Soft deleted users
    async def get_soft_deleted_users(
        self, offset: int = 0, limit: int = 50
    ) -> list[User]: ...

    # Filter & count
    async def get_users_by_filter(
        self, filters: dict, offset: int = 0, limit: int = 50
    ) -> list[User]: ...

    async def count_users(self, is_active: bool | None = None) -> int: ...
