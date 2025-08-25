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
        session_data = session_in.model_dump()
        session_data["expires_at"] = expires_at
        session_obj = SessionCreate(**session_data)
        db_obj = await self.session_repo.create_session(session_obj)
        return SessionInDB.model_validate(db_obj, from_attributes=True)

    async def deactivate_session(self, session_id: int) -> bool:
        """Deactivate (invalidate) a session."""
        return await self.session_repo.deactivate_session(session_id)

    async def delete_session(self, session_id: int) -> bool:
        """Delete a session permanently."""
        return await self.session_repo.delete_session(session_id)

    async def get_session(self, session_id: int) -> SessionInDB | None:
        """Get session by its ID."""
        db_obj = await self.session_repo.get_session(session_id)
        if db_obj is None:
            return None
        return SessionInDB.model_validate(db_obj, from_attributes=True)

    async def get_sessions_by_user(self, user_id: str) -> list[SessionInDB]:
        """Get all sessions for a user."""
        db_objs = await self.session_repo.get_sessions_by_user(user_id)
        return [
            SessionInDB.model_validate(obj, from_attributes=True) for obj in db_objs
        ]

    async def get_active_sessions(self, user_id: str) -> list[SessionInDB]:
        """Get all active sessions for a user.

        Args:
            user_id: The string UUID of the user.

        Returns:
            List of active SessionInDB objects.
        """
        db_objs = await self.session_repo.get_active_sessions(user_id)
        return [
            SessionInDB.model_validate(obj, from_attributes=True) for obj in db_objs
        ]

    async def activate_session(self, session_id: int) -> bool:
        """Activate a session by its ID.

        Args:
            session_id: The integer ID of the session.

        Returns:
            True if activation was successful, False otherwise.
        """
        return await self.session_repo.activate_session(session_id)

    async def delete_all_user_sessions(self, user_id: str) -> int:
        """Delete all sessions for a given user.

        Args:
            user_id: The string UUID of the user.

        Returns:
            The number of sessions deleted.
        """
        return await self.session_repo.delete_all_user_sessions(user_id)

    async def purge_expired_sessions(self) -> int:
        """Delete all expired sessions.

        Returns:
            The number of sessions deleted.
        """
        return await self.session_repo.purge_expired_sessions()

    async def update_session_activity(
        self, session_id: int, ip_address: str, user_agent: str
    ) -> bool:
        """Update session activity info (IP, user agent).

        Args:
            session_id: The integer ID of the session.
            ip_address: The IP address to update.
            user_agent: The user agent string to update.

        Returns:
            True if update was successful, False otherwise.
        """
        return await self.session_repo.update_session_activity(
            session_id, ip_address, user_agent
        )
