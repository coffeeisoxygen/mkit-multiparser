from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.intf_user import IUserRepository
from app.models.db_user import User
from app.schemas.user.sch_user import UserCreate, UserUpdate


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    # CRUD Methods
    async def create_user(self, user_in: UserCreate) -> User:
        # Ambil password yang sudah di-hash dari service
        user_data = user_in.model_dump(exclude={"password"})
        db_user = User(**user_data, hashed_password=user_in.password)
        self.session.add(db_user)
        await self.session.flush()
        return db_user

    async def get_user_with_id(self, user_id: str) -> User | None:
        return await self.session.get(User, user_id)

    async def get_user_with_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_with_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user(self, user_id: str, user_in: UserUpdate) -> User | None:
        db_user = await self.session.get(User, user_id)
        if not db_user:
            return None

        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        await self.session.flush()
        return db_user

    async def delete_user(self, user_id: str) -> bool:
        db_user = await self.session.get(User, user_id)
        if not db_user:
            return False
        await self.session.delete(db_user)
        await self.session.flush()
        return True

    # Status/Role Management Methods
    async def change_password(self, user_id: str, new_password: str) -> bool:
        db_user = await self.session.get(User, user_id)
        if not db_user:
            return False
        db_user.hashed_password = new_password
        await self.session.flush()
        return True

    async def activate_user(self, user_id: str) -> User | None:
        db_user = await self.session.get(User, user_id)
        if not db_user:
            return None
        db_user.is_active = True
        await self.session.flush()
        return db_user

    async def deactivate_user(self, user_id: str) -> User | None:
        db_user = await self.session.get(User, user_id)
        if not db_user:
            return None
        db_user.is_active = False
        await self.session.flush()
        return db_user

    async def soft_delete_user(self, user_id: str) -> User | None:
        db_user = await self.session.get(User, user_id)
        if not db_user:
            return None
        db_user.is_active = False
        db_user.deleted_at = datetime.now(UTC)
        await self.session.flush()
        return db_user

    async def restore_user(self, user_id: str) -> User | None:
        db_user = await self.session.get(User, user_id)
        if not db_user:
            return None
        db_user.is_active = True
        db_user.deleted_at = None
        await self.session.flush()
        return db_user

    async def set_superuser(self, user_id: str) -> User | None:
        db_user = await self.session.get(User, user_id)
        if not db_user:
            return None
        db_user.is_superuser = True
        await self.session.flush()
        return db_user

    async def unset_superuser(self, user_id: str) -> User | None:
        db_user = await self.session.get(User, user_id)
        if not db_user:
            return None
        db_user.is_superuser = False
        await self.session.flush()
        return db_user

    # Query/Filter Methods
    async def get_all_users(
        self, offset: int = 0, limit: int = 50, is_active: bool | None = None
    ) -> list[User]:
        stmt = select(User).offset(offset).limit(limit).order_by(User.created_at)
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_superusers(self, offset: int = 0, limit: int = 50) -> list[User]:
        stmt = select(User).where(User.is_superuser).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_soft_deleted_users(
        self, offset: int = 0, limit: int = 50
    ) -> list[User]:
        stmt = select(User).where(User.is_active.is_(False)).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_users_by_filter(
        self, filters: dict, offset: int = 0, limit: int = 50
    ) -> list[User]:
        stmt = select(User)
        for key, value in filters.items():
            if hasattr(User, key):
                stmt = stmt.where(getattr(User, key) == value)
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # Utility Methods
    async def count_users(self, is_active: bool | None = None) -> int:
        stmt = select(User)
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())
