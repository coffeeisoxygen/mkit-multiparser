from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.user.sch_user import UserAdminResponse


class SessionBase(BaseModel):
    """Schema dasar dengan atribut umum session."""

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="forbid"
    )

    user_id: int
    is_active: bool
    expires_at: datetime


class SessionCreate(BaseModel):
    """Schema untuk membuat sesi baru."""

    user_id: int
    token: str
    ip_address: str
    user_agent: str


class SessionInDB(SessionBase):
    """Schema representasi session di database (internal)."""

    id: int
    token: str  # hanya internal
    ip_address: str
    user_agent: str
    created_at: datetime
    updated_at: datetime


class SessionPublicResponse(SessionBase):
    """Schema response untuk user biasa (public).

    Tidak expose token, ip, user agent.
    """

    id: int
    created_at: datetime
    updated_at: datetime


class SessionAdminResponse(SessionBase):
    """Schema response untuk admin.

    Expose field sensitif (ip + user agent).
    """

    id: int
    user: UserAdminResponse | None = None
    ip_address: str | None
    user_agent: str | None
    created_at: datetime
    updated_at: datetime
