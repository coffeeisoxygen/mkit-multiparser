from datetime import datetime

from pydantic import BaseModel


class CreateUpdateMixin(BaseModel):
    created_at: datetime | None
    updated_at: datetime | None


class SoftDeleteMixin(BaseModel):
    deleted_at: datetime | None
