from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.db_audit import TimestampMixin


class Session(Base, TimestampMixin):
    """Session model for tracking user sessions.

    Attributes:
        id (str): Primary key, UUID string.
        user_id (str): Foreign key to User.id (UUID).
        token (str): Session token, unique.
        ip_address (str): IP address of the session.
        user_agent (str): User agent string.
        last_activity (datetime): Last activity timestamp.
        is_active (bool): Session active status.
        user (User): Relationship to User.
    """

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    ip_address: Mapped[str] = mapped_column(String)
    user_agent: Mapped[str] = mapped_column(String)
    last_activity: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship("User", back_populates="sessions")
