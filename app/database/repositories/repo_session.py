# ...existing code...
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.intf_session import ISessionRepository
from app.models import Session
from app.schemas.user.sch_user_session import SessionCreate


def _ensure_utc(dt: datetime) -> datetime:
    """Ensure datetime is offset-aware UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


class SessionRepository(ISessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_session(self, session_id: int) -> Session | None:
        return await self.session.get(Session, session_id)

    async def get_sessions_by_user(self, user_id: int) -> list[Session]:
        stmt = select(Session).where(Session.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_session(self, session_in: SessionCreate) -> Session:
        """Create a new session, ensuring expires_at is always set and offset-aware UTC.

        If expires_at is not provided, set to now + 1 hour.
        """
        data = session_in.model_dump()
        # Ensure user_id is always str
        data["user_id"] = str(data["user_id"])
        # Set default expiry if not provided
        expires_at = data.get("expires_at")
        if expires_at is None:
            expires_at = datetime.now(tz=UTC) + timedelta(hours=1)
        expires_at = _ensure_utc(expires_at)
        data["expires_at"] = expires_at
        db_session = Session(**data)
        self.session.add(db_session)
        await self.session.flush()
        return db_session

    async def delete_session(self, session_id: int) -> bool:
        db_session = await self.session.get(Session, session_id)
        if not db_session:
            return False
        await self.session.delete(db_session)
        await self.session.flush()
        return True

    async def delete_all_user_sessions(self, user_id: int) -> int:
        stmt = delete(Session).where(Session.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.rowcount or 0

    # 🔥 Extra methods

    async def activate_session(self, session_id: int) -> bool:
        stmt = update(Session).where(Session.id == session_id).values(is_active=True)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def deactivate_session(self, session_id: int) -> bool:
        stmt = update(Session).where(Session.id == session_id).values(is_active=False)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def get_active_sessions(self, user_id: int) -> list[Session]:
        stmt = select(Session).where(Session.user_id == user_id, Session.is_active)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def purge_expired_sessions(self) -> int:
        """Hapus semua session yang sudah expired."""
        now = datetime.now(tz=UTC)
        now = _ensure_utc(now)
        # Ensure all Session.expires_at are offset-aware for comparison
        # This is a workaround for SQLite and test assignment issues
        # Use a subquery to select expired session ids, then delete by id
        expired_ids = []
        stmt = select(Session.id, Session.expires_at)
        result = await self.session.execute(stmt)
        for session_id, expires_at in result.all():
            # Convert expires_at to UTC if naive
            if expires_at is not None:
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=UTC)
                else:
                    expires_at = expires_at.astimezone(UTC)
                if expires_at < now:
                    expired_ids.append(session_id)
        if not expired_ids:
            return 0
        del_stmt = delete(Session).where(Session.id.in_(expired_ids))
        del_result = await self.session.execute(del_stmt)
        return del_result.rowcount or 0

    async def update_session_activity(
        self, session_id: int, ip_address: str, user_agent: str
    ) -> bool:
        stmt = (
            update(Session)
            .where(Session.id == session_id)
            .values(ip_address=ip_address, user_agent=user_agent)
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0
