"""Schema untuk response token dan login user."""

from pydantic import BaseModel

from app.schemas.user.sch_user import UserRead


class TokenResponse(BaseModel):
    """Schema untuk JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserLoginResponse(BaseModel):
    """Schema untuk response login user + token."""

    user: UserRead
    token: TokenResponse
    is_active: bool
    is_superuser: bool


class UserLoginRequest(BaseModel):
    """Schema untuk request login user."""

    username: str
    password: str
