"""schema untuk user."""

# ...existing code...
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# The core user attributes
class UserBase(BaseModel):
    """UserBase schema for core user attributes.

    This schema defines the basic attributes for a user, which are
    common across different user-related operations.

    Args:
        BaseModel (_type_): Schema for core user attributes.
    """

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="forbid"
    )
    username: str
    email: str
    full_name: str


class UserCreate(UserBase):
    """UserCreate schema for creating a new user.

    This schema extends the UserBase schema by adding the required
    password field for user registration.

    Args:
        UserBase (_type_): Schema for creating a new user.
    """

    password: str


class UserUpdate(BaseModel):
    """UserUpdate schema for updating user details.

    This schema allows partial updates to user attributes.

    Args:
        BaseModel (_type_): Schema for updating user details (input for PATCH /users/{id}).

    """

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="forbid"
    )
    email: str | None = None
    full_name: str | None = None


class UserUpdatePassword(UserUpdate):
    """UserUpdatePassword schema for updating user password.

    This schema extends the UserUpdate schema by adding fields
    specific to password updates.

    Args:
        UserUpdate (_type_): Schema for updating user password.
    """

    old_password: str
    new_password: str
    confirm_password: str


class UserInDB(UserBase):
    """UserInDB schema for representing a user in the database.

    This schema extends the UserBase schema by adding fields
    specific to database representation.

    Args:
        UserBase (_type_): Schema for a full user object, including sensitive data (internal use)
    """

    id: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None


class UserPublicResponse(UserBase):
    """UserPublicResponse schema for public user information.

    This schema is used to expose user information to API clients,
    omitting sensitive data such as passwords.

    Args:
        UserBase (_type_): Schema for public user information.
    """

    id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None


class UserAdminResponse(UserPublicResponse):
    """UserAdminResponse schema for representing an admin user.

    This schema is used to expose admin user information to API clients.

    Args:
        UserPublicResponse (_type_): Schema for public user information.
    """

    is_active: bool
    is_superuser: bool


class UserSoftDeletedRead(BaseModel):
    """UserSoftDeletedRead schema for representing a soft-deleted user.

    This schema is used to expose soft-deleted user information to API clients.

    Args:
        BaseModel (_type_): Schema for representing a soft-deleted user.
    """

    id: str
    email: str
    deleted_at: datetime
