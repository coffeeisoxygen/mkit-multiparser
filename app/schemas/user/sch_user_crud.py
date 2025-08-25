"""schema untuk user."""

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from app.models.db_user import SoftDeleteMixin
from app.schemas.user.sch_user_base import CreateUpdateMixin, UserBase


class UserCreate(UserBase):
    """UserCreate schema for creating a new user.

    This schema extends the UserBase schema by adding the required
    password field for user registration.

    Args:
        UserBase (_type_): Schema for creating a new user.
    """

    password: str = Field(
        description="password",
        min_length=6,
        pattern=r"^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]+$",
    )


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


class UserUpdatePassword(BaseModel):
    """UserUpdatePassword schema for updating user password.

    This schema is focused only on password update fields.

    Args:
        BaseModel (_type_): Schema for updating user password.
    """

    old_password: str
    new_password: str
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        """Validates that confirm_password matches new_password.

        Args:
            v (str): The value of confirm_password.
            info (ValidationInfo): Validation context.

        Returns:
            str: The validated confirm_password.

        Raises:
            ValueError: If confirm_password does not match new_password.
        """
        new_password = info.data.get("new_password")
        if new_password is not None and v != new_password:
            raise ValueError("Passwords do not match")
        return v


class UserInDB(UserBase, CreateUpdateMixin, SoftDeleteMixin):
    """UserInDB schema for representing a user in the database.

    This schema extends the UserBase schema by adding fields
    specific to database representation.

    Args:
        UserBase (_type_): Schema for a full user object, including sensitive data (internal use)
    """

    id: int
    hashed_password: str
    is_active: bool
    is_superuser: bool
