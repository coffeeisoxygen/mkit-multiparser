from sqlalchemy import JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base
from app.models.hlp_mixin import TimestampMixin


class AuditLog(Base, TimestampMixin):
    """Audit log generic & reusable."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    description: Mapped[dict | str] = mapped_column(JSON, nullable=False)
    detail: Mapped[JSON | None] = mapped_column(JSON, nullable=True)
