from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TokenResponse(BaseModel):
    """Schema untuk JWT token response ke client."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserLoginRequest(BaseModel):
    """Schema untuk request login user."""

    username: str
    password: str


class UserLoginResponse(BaseModel):
    """Schema untuk response login user + token."""

    # data user (public info)
    id: UUID
    username: str
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool

    # token
    token: TokenResponse


class TokenPayload(BaseModel):
    """Schema payload yang ada di dalam JWT.

    sub = username (string, immutable, unique).
    """

    model_config = ConfigDict(from_attributes=True)
    sub: str
    is_superuser: bool
    is_active: bool
    exp: datetime
