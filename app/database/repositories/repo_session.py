import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.intf_session import ISessionRepository
from app.models import Session
from app.schemas.session.sch_session import SessionCreate


class SessionRepository(ISessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_session(self, session_id: uuid.UUID) -> Session | None:
        return await self.session.get(Session, str(session_id))

    async def get_sessions_by_user(self, user_id: uuid.UUID) -> list[Session]:
        stmt = select(Session).where(Session.user_id == str(user_id))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_session(self, session_in: SessionCreate) -> Session:
        db_session = Session(**session_in.model_dump())
        self.session.add(db_session)
        await self.session.flush()
        return db_session

    async def delete_session(self, session_id: uuid.UUID) -> bool:
        db_session = await self.session.get(Session, str(session_id))
        if not db_session:
            return False
        await self.session.delete(db_session)
        await self.session.flush()
        return True

    async def delete_all_user_sessions(self, user_id: uuid.UUID) -> int:
        stmt = delete(Session).where(Session.user_id == str(user_id))
        result = await self.session.execute(stmt)
        return result.rowcount or 0
