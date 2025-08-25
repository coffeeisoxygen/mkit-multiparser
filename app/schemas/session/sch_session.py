import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.user.sch_user import UserAdminResponse


class SessionBase(BaseModel):
    """Schema dasar dengan atribut-atribut yang umum untuk semua skema sesi."""

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="forbid"
    )

    user_id: uuid.UUID
    token: str
    ip_address: str
    user_agent: str
    is_active: bool
    expires_at: datetime


class SessionCreate(BaseModel):
    """Schema untuk membuat sesi baru."""

    token: str
    user_id: uuid.UUID
    ip_address: str
    user_agent: str


class SessionInDB(SessionBase):
    """Schema yang mewakili data sesi seperti yang disimpan di database.

    Ini digunakan untuk konversi dari model ORM ke Pydantic.
    """

    id: int
    created_at: datetime
    updated_at: datetime


class SessionPublicResponse(SessionBase):
    """Schema untuk respons publik session (user biasa).

    Hanya expose data non-sensitif.
    """

    id: int
    created_at: datetime
    updated_at: datetime


class SessionAdminResponse(SessionBase):
    """Schema untuk respons admin session.

    Expose semua field, termasuk IP dan user agent.
    """

    id: int
    user: UserAdminResponse | None = None
    created_at: datetime
    updated_at: datetime
    ip_address: str
    user_agent: str
