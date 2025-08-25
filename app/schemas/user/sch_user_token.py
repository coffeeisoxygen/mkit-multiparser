from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.schemas.user.sch_user import UserPublicResponse


class UserLoginRequest(BaseModel):
    """Schema untuk request login user."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema untuk JWT token response ke client."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # detik


class UserLoginResponse(BaseModel):
    """Schema untuk response login user + token.

    User info = UserPublicResponse (tanpa field sensitif).
    """

    user: UserPublicResponse
    token: TokenResponse


class TokenPayload(BaseModel):
    """Schema payload yang ada di dalam JWT (internal use only).

    sub = biasanya user_id (lebih aman dari username).
    """

    sub: str | int  # bisa user_id atau username, prefer user_id
    exp: datetime
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)
