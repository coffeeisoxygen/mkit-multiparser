import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
    """Schema untuk respons publik, mengecualikan data sensitif.

    seperti IP address jika tidak diperlukan.
    """

    id: int
    created_at: datetime
    updated_at: datetime
