"""Session repository interface definitions.

This module defines the ISessionRepository protocol, which specifies
the contract for session-related database operations. Implementations
should provide asynchronous methods for CRUD and session management.
"""

import uuid
from typing import Protocol

from app.models import Session
from app.schemas.session.sch_session import SessionCreate


class ISessionRepository(Protocol):
    """Protocol for session repository operations.

    This interface defines asynchronous methods for retrieving,
    creating, and deleting session records.
    """

    async def get_session(self, session_id: uuid.UUID) -> Session | None:
        """Retrieve a session by its unique ID.

        Args:
            session_id: The UUID of the session.

        Returns:
            The Session object if found, otherwise None.
        """
        ...

    async def get_sessions_by_user(self, user_id: uuid.UUID) -> list[Session]:
        """Retrieve all sessions for a given user.

        Args:
            user_id: The UUID of the user.

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

    async def delete_session(self, session_id: uuid.UUID) -> bool:
        """Delete a session by its unique ID.

        Args:
            session_id: The UUID of the session to delete.

        Returns:
            True if deletion was successful, False otherwise.
        """
        ...

    async def delete_all_user_sessions(self, user_id: uuid.UUID) -> int:
        """Delete all sessions for a given user.

        Args:
            user_id: The UUID of the user.

        Returns:
            The number of sessions deleted.
        """
        ...
