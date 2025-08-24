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
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None


class UserDeactivate(UserBase):
    pass
