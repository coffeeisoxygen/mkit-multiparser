from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateUpdateMixin(BaseModel):
    created_at: datetime | None
    updated_at: datetime | None


class SoftDeleteMixin(BaseModel):
    deleted_at: datetime | None


class UserBase(BaseModel):
    """UserBase schema for core user attributes.

    Common attributes for user-related operations.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
    username: str = Field(
        description="username", min_length=2, pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: str = Field(description="email", pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    full_name: str = Field(
        description="full name", min_length=2, pattern=r"^[a-zA-Z\s]+$"
    )


class UserPublicResponse(UserBase):
    """UserPublicResponse schema for public user information.

    Expose only non-sensitive user info.
    """

    id: int


class UserAdminResponse(UserPublicResponse):
    """UserAdminResponse schema for admin user info.

    Expose is_active and is_superuser fields.
    """

    is_active: bool
    is_superuser: bool


class UserSoftDeletedResponse(CreateUpdateMixin, SoftDeleteMixin):
    """UserSoftDeletedRead schema for representing a soft-deleted user.

    This schema is used to expose soft-deleted user information to API clients.

    Args:
        BaseModel (_type_): Schema for representing a soft-deleted user.
    """

    id: int
    username: str
    email: str
