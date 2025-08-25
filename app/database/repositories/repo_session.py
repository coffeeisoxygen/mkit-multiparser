# ...existing code...
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.intf_session import ISessionRepository
from app.models import Session
from app.schemas.session.sch_session import SessionCreate


class SessionRepository(ISessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_session(self, session_id: int) -> Session | None:
        return await self.session.get(Session, session_id)

    async def get_sessions_by_user(self, user_id: str) -> list[Session]:
        stmt = select(Session).where(Session.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_session(self, session_in: SessionCreate) -> Session:
        """Create a new session, ensuring expires_at is always set.

        If expires_at is not provided, set to now + 1 hour.
        """
        data = session_in.model_dump()
        # Ensure user_id is always str
        data["user_id"] = str(data["user_id"])
        # Set default expiry if not provided
        if "expires_at" not in data or data["expires_at"] is None:
            data["expires_at"] = datetime.now(tz=UTC) + timedelta(hours=1)
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

    async def delete_all_user_sessions(self, user_id: str) -> int:
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

    async def get_active_sessions(self, user_id: str) -> list[Session]:
        stmt = select(Session).where(Session.user_id == user_id, Session.is_active)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def purge_expired_sessions(self) -> int:
        """Hapus semua session yang sudah expired."""
        now = datetime.now(tz=UTC)
        stmt = delete(Session).where(Session.expires_at < now)
        result = await self.session.execute(stmt)
        return result.rowcount or 0

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
