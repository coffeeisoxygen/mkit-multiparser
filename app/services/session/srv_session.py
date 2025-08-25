from datetime import datetime, timedelta

from loguru import logger

from app.database.repositories.intf_session import ISessionRepository
from app.exception import SessionLimitExceededError
from app.schemas.user.sch_user_session import SessionCreate, SessionInDB


class SessionService:
    """Service layer for session management."""

    def __init__(
        self,
        session_repo: ISessionRepository,
        default_expiry_minutes: int = 60,
        max_active_sessions_per_user: int = 3,  # default limit
    ):
        self.session_repo = session_repo
        self.default_expiry_minutes = default_expiry_minutes
        self.max_active_sessions_per_user = max_active_sessions_per_user

    async def create_session(
        self, session_in: SessionCreate, expiry_minutes: int | None = None
    ) -> SessionInDB:
        """Create a new session with calculated expiry.

        #NOTE: Future - add session type, deactivation reason, last_activity_at
        """
        user_id = session_in.user_id
        try:
            active_sessions = await self.get_active_sessions(user_id)
            if len(active_sessions) >= self.max_active_sessions_per_user:
                logger.warning(
                    f"User {user_id} exceeded max active sessions ({self.max_active_sessions_per_user})"
                )
                raise SessionLimitExceededError(
                    f"Max active sessions ({self.max_active_sessions_per_user}) exceeded for user {user_id}"
                )
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
            logger.info(f"Session created for user {user_id}")
            return SessionInDB.model_validate(db_obj, from_attributes=True)
        except SessionLimitExceededError:
            raise
        except Exception as e:
            logger.error(f"Failed to create session for user {user_id}: {e}")
            raise

    async def deactivate_session(self, session_id: int) -> bool:
        """Deactivate (invalidate) a session.
        #NOTE: Future - log deactivation reason
        """
        try:
            result = await self.session_repo.deactivate_session(session_id)
            logger.info(f"Session {session_id} deactivated")
            return result
        except Exception as e:
            logger.error(f"Failed to deactivate session {session_id}: {e}")
            raise

    async def delete_session(self, session_id: int) -> bool:
        """Delete a session permanently.
        #NOTE: Future - log deletion reason
        """
        try:
            result = await self.session_repo.delete_session(session_id)
            logger.info(f"Session {session_id} deleted")
            return result
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            raise

    async def get_session(self, session_id: int) -> SessionInDB | None:
        """Get session by its ID."""
        try:
            db_obj = await self.session_repo.get_session(session_id)
            if db_obj is None:
                logger.info(f"Session {session_id} not found")
                return None
            logger.info(f"Session {session_id} retrieved")
            return SessionInDB.model_validate(db_obj, from_attributes=True)
        except Exception as e:
            logger.error(f"Failed to get session {session_id}: {e}")
            raise

    async def get_sessions_by_user(self, user_id: int) -> list[SessionInDB]:
        """Get all sessions for a user."""
        try:
            db_objs = await self.session_repo.get_sessions_by_user(user_id)
            logger.info(f"Retrieved {len(db_objs)} sessions for user {user_id}")
            return [
                SessionInDB.model_validate(obj, from_attributes=True) for obj in db_objs
            ]
        except Exception as e:
            logger.error(f"Failed to get sessions for user {user_id}: {e}")
            raise

    async def get_active_sessions(self, user_id: int) -> list[SessionInDB]:
        """Get all active sessions for a user.

        Args:
            user_id: The integer ID of the user.

        Returns:
            List of active SessionInDB objects.
        """
        try:
            db_objs = await self.session_repo.get_active_sessions(user_id)
            logger.info(f"Retrieved {len(db_objs)} active sessions for user {user_id}")
            return [
                SessionInDB.model_validate(obj, from_attributes=True) for obj in db_objs
            ]
        except Exception as e:
            logger.error(f"Failed to get active sessions for user {user_id}: {e}")
            raise

    async def activate_session(self, session_id: int) -> bool:
        """Activate a session by its ID.

        Args:
            session_id: The integer ID of the session.

        Returns:
            True if activation was successful, False otherwise.
        """
        try:
            result = await self.session_repo.activate_session(session_id)
            logger.info(f"Session {session_id} activated")
            return result
        except Exception as e:
            logger.error(f"Failed to activate session {session_id}: {e}")
            raise

    async def delete_all_user_sessions(self, user_id: int) -> int:
        """Delete all sessions for a given user.

        Args:
            user_id: The integer ID of the user.

        Returns:
            The number of sessions deleted.
        """
        try:
            result = await self.session_repo.delete_all_user_sessions(user_id)
            logger.info(f"Deleted {result} sessions for user {user_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to delete all sessions for user {user_id}: {e}")
            raise

    async def purge_expired_sessions(self) -> int:
        """Delete all expired sessions.

        Returns:
            The number of sessions deleted.
        """
        try:
            result = await self.session_repo.purge_expired_sessions()
            logger.info(f"Purged {result} expired sessions")
            return result
        except Exception as e:
            logger.error(f"Failed to purge expired sessions: {e}")
            raise

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
        try:
            result = await self.session_repo.update_session_activity(
                session_id, ip_address, user_agent
            )
            logger.info(
                f"Session {session_id} activity updated (IP: {ip_address}, UA: {user_agent})"
            )
            return result
        except Exception as e:
            logger.error(f"Failed to update activity for session {session_id}: {e}")
            raise
