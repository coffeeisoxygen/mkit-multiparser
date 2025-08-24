"""schema untuk user."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="forbid"
    )

    username: str
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str


class UserSeedAdmin(UserBase):
    is_superuser: bool
    is_active: bool


class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="forbid"
    )
    email: str | None
    full_name: str | None


class UserUpdatePassword(UserUpdate):
    old_password: str
    new_password: str
    confirm_password: str


class UserSoftDeletedRead(BaseModel):
    """Schema minimal untuk user yang sudah soft delete.

    Hanya berisi id, deleted_at, dan email.
    Digunakan untuk response user yang statusnya sudah dihapus (soft delete).
    """

    id: uuid.UUID
    deleted_at: datetime | None
    email: str
