import uuid
from datetime import datetime
from typing import Protocol

from app.schemas.session.sch_session import SessionCreate, SessionInDB


class ISessionRepository(Protocol):
    async def get_session_by_id(self, session_id: int) -> SessionInDB | None:
        """Get session by its ID."""
        ...

    async def get_session_by_token(self, token: str) -> SessionInDB | None:
        """Get session by token."""
        ...

    async def get_sessions_by_user_id(
        self, user_id: uuid.UUID, is_active: bool | None = None
    ) -> list[SessionInDB]:
        """Get all sessions for a user, optionally filter by active status."""
        ...

    async def create_session(
        self, session_in: SessionCreate, expires_at: datetime
    ) -> SessionInDB:
        """Create a new session."""
        ...

    async def deactivate_session(self, session_id: int) -> bool:
        """Deactivate (invalidate) a session."""
        ...

    async def delete_session(self, session_id: int) -> bool:
        """Delete a session permanently."""
        ...
