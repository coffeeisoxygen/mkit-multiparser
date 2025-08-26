from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.interfaces.iuser_repo import IUserRepository
from app.models.db_user import User as Db_User


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj_in: dict) -> Db_User:
        db_user = Db_User(**obj_in)
        self.session.add(db_user)
        await self.session.flush()
        return db_user

    async def get_by_id(self, obj_id: int) -> Db_User | None:
        stmt = select(Db_User).where(Db_User.id == obj_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list(self, offset: int = 0, limit: int = 50) -> list[Db_User]:
        stmt = select(Db_User).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update(self, obj_id: int, obj_in: dict) -> Db_User | None:
        db_user = await self.get_by_id(obj_id)
        if not db_user:
            return None
        for k, v in obj_in.items():
            setattr(db_user, k, v)
        await self.session.flush()
        return db_user

    async def delete(self, obj_id: int) -> bool:
        db_user = await self.get_by_id(obj_id)
        if not db_user:
            return False
        await self.session.delete(db_user)
        await self.session.flush()
        return True

    async def get_by_username(self, username: str) -> Db_User | None:
        stmt = select(Db_User).where(Db_User.username == username)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Db_User | None:
        stmt = select(Db_User).where(Db_User.email == email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
