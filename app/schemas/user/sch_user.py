"""schema untuk user."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserInDB(BaseModel):
    """Schema untuk user yang ada di database.

    schema ini di gunakan untuk mapping tipe kembalian data. agar tidak terjadi kesalahan tipe data. dan meminimalisir mapping di service layer.

    Args:
        UserBase (BaseModel): shared Fields for user.

    Returns:
        UserInDB: user yang ada di database.
    """

    id: uuid.UUID
    username: str
    email: str
    full_name: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None


class UserBase(BaseModel):
    """shared Fields for user."""

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="forbid"
    )

    username: str
    email: str
    full_name: str


class UserCreate(UserBase):
    """inherit from UserBase, dengan tambahan password."""

    password: str


class UserPublicResponse(UserBase):
    """response public untuk user.

    ini di gunakan jika butuh schema response yang lebih ringan.
    most cases, ini di gunakan untuk response yang tidak memerlukan informasi sensitif.
    """

    id: uuid.UUID


class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool
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
