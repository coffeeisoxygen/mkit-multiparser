import uuid
from datetime import datetime, timedelta

from app.database.repositories.intf_session import ISessionRepository
from app.schemas.session.sch_session import SessionCreate, SessionInDB


class SessionService:
    """Service layer for session management."""

    def __init__(
        self, session_repo: ISessionRepository, default_expiry_minutes: int = 60
    ):
        self.session_repo = session_repo
        self.default_expiry_minutes = default_expiry_minutes

    async def create_session(
        self, session_in: SessionCreate, expiry_minutes: int | None = None
    ) -> SessionInDB:
        """Create a new session with calculated expiry."""
        minutes = (
            expiry_minutes
            if expiry_minutes is not None
            else self.default_expiry_minutes
        )
        expires_at = datetime.now() + timedelta(minutes=minutes)
        return await self.session_repo.create_session(session_in, expires_at)

    async def deactivate_session(self, session_id: int) -> bool:
        """Deactivate (invalidate) a session."""
        return await self.session_repo.deactivate_session(session_id)

    async def delete_session(self, session_id: int) -> bool:
        """Delete a session permanently."""
        return await self.session_repo.delete_session(session_id)

    async def get_session_by_id(self, session_id: int) -> SessionInDB | None:
        """Get session by its ID."""
        return await self.session_repo.get_session_by_id(session_id)

    async def get_session_by_token(self, token: str) -> SessionInDB | None:
        """Get session by token."""
        return await self.session_repo.get_session_by_token(token)

    async def get_sessions_by_user_id(
        self, user_id: uuid.UUID, is_active: bool | None = None
    ) -> list[SessionInDB]:
        """Get all sessions for a user, optionally filter by active status."""
        return await self.session_repo.get_sessions_by_user_id(user_id, is_active)
