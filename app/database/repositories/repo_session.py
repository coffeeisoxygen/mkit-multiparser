import uuid
from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_sessions import Session as SessionModel
from app.schemas.session.sch_session import SessionCreate, SessionInDB


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_session_by_id(self, session_id: int) -> SessionInDB | None:
        db_session = await self.session.get(SessionModel, session_id)
        return SessionInDB.model_validate(db_session) if db_session else None

    async def get_session_by_token(self, token: str) -> SessionInDB | None:
        stmt = select(SessionModel).where(SessionModel.token == token)
        result = await self.session.execute(stmt)
        db_session = result.scalar_one_or_none()
        return SessionInDB.model_validate(db_session) if db_session else None

    async def get_sessions_by_user_id(
        self, user_id: uuid.UUID, is_active: bool | None = None
    ) -> list[SessionInDB]:
        stmt = select(SessionModel).where(SessionModel.user_id == str(user_id))
        if is_active is not None:
            stmt = stmt.where(SessionModel.is_active == is_active)
        result = await self.session.execute(stmt)
        sessions = result.scalars().all()
        return [SessionInDB.model_validate(s) for s in sessions]

    async def create_session(
        self, session_in: SessionCreate, expires_at: datetime
    ) -> SessionModel:
        data = session_in.model_dump()
        db_session = SessionModel(**data, expires_at=expires_at)
        self.session.add(db_session)
        await self.session.flush()
        return db_session

    async def deactivate_session(self, session_id: int) -> SessionModel | None:
        db_session = await self.session.get(SessionModel, session_id)
        if not db_session:
            return None
        db_session.is_active = False
        await self.session.flush()
        return db_session

    async def delete_session(self, session_id: int) -> int:
        stmt = delete(SessionModel).where(SessionModel.id == session_id)
        result = await self.session.execute(stmt)
        return result.rowcount
