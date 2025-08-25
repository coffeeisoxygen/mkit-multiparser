"""Session repository interface definitions.

This module defines the ISessionRepository protocol, which specifies
the contract for session-related database operations. Implementations
should provide asynchronous methods for CRUD and session management.
"""

from typing import Protocol

from app.models import Session
from app.schemas.session.sch_session import SessionCreate


class ISessionRepository(Protocol):
    """Protocol for session repository operations.

    This interface defines asynchronous methods for retrieving,
    creating, and deleting session records.
    """

    async def get_session(self, session_id: int) -> Session | None:
        """Retrieve a session by its unique ID.

        Args:
            session_id: The integer ID of the session.

        Returns:
            The Session object if found, otherwise None.
        """
        ...

    async def get_sessions_by_user(self, user_id: str) -> list[Session]:
        """Retrieve all sessions for a given user.

        Args:
            user_id: The string UUID of the user.

        Returns:
            A list of Session objects.
        """
        ...

    async def create_session(self, session_in: SessionCreate) -> Session:
        """Create a new session record.

        Args:
            session_in: The data required to create a session.

        Returns:
            The created Session object.
        """
        ...

    async def delete_session(self, session_id: int) -> bool:
        """Delete a session by its unique ID.

        Args:
            session_id: The integer ID of the session to delete.

        Returns:
            True if deletion was successful, False otherwise.
        """
        ...

    async def delete_all_user_sessions(self, user_id: str) -> int:
        """Delete all sessions for a given user.

        Args:
            user_id: The string UUID of the user.

        Returns:
            The number of sessions deleted.
        """
        ...

    async def activate_session(self, session_id: int) -> bool:
        """Activate a session by its ID."""
        ...

    async def deactivate_session(self, session_id: int) -> bool:
        """Deactivate a session by its ID."""
        ...

    async def get_active_sessions(self, user_id: str) -> list[Session]:
        """Get all active sessions for a user."""
        ...

    async def purge_expired_sessions(self) -> int:
        """Delete all expired sessions."""
        ...

    async def update_session_activity(
        self, session_id: int, ip_address: str, user_agent: str
    ) -> bool:
        """Update session activity info (IP, user agent)."""
        ...
