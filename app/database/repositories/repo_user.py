from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.intf_user import IUserRepository
from app.models.db_user import User as Db_User
from app.schemas import UserCreate, UserInDB, UserUpdate


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    # CRUD Methods
    async def create_user(self, user_in: UserCreate) -> UserInDB:
        hashed_password = user_in.password
        db_user = Db_User(**user_in.model_dump(), hashed_password=hashed_password)
        self.session.add(db_user)
        await self.session.flush()
        return UserInDB.model_validate(db_user)

    async def get_user_with_id(self, user_id: int) -> UserInDB | None:
        db_user = await self.session.get(Db_User, user_id)
        if db_user:
            return UserInDB.model_validate(db_user)
        return None

    async def get_user_with_username(self, username: str) -> UserInDB | None:
        stmt = select(Db_User).where(Db_User.username == username)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user:
            return UserInDB.model_validate(db_user)
        return None

    async def get_user_with_email(self, email: str) -> UserInDB | None:
        stmt = select(Db_User).where(Db_User.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        if db_user:
            return UserInDB.model_validate(db_user)
        return None

    async def update_user(self, user_id: int, user_in: UserUpdate) -> UserInDB | None:
        db_user = await self.session.get(Db_User, user_id)
        if not db_user:
            return None

        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        await self.session.flush()
        return UserInDB.model_validate(db_user)

    async def delete_user(self, user_id: int) -> bool:
        db_user = await self.session.get(Db_User, user_id)
        if not db_user:
            return False
        await self.session.delete(db_user)
        await self.session.flush()
        return True

    # Status/Role Management Methods
    async def change_password(self, user_id: int, new_password: str) -> bool:
        db_user = await self.session.get(Db_User, user_id)
        if not db_user:
            return False
        db_user.hashed_password = new_password
        await self.session.flush()
        return True

    async def activate_user(self, user_id: int) -> UserInDB | None:
        db_user = await self.session.get(Db_User, user_id)
        if not db_user:
            return None
        db_user.is_active = True
        await self.session.flush()
        return UserInDB.model_validate(db_user)

    async def deactivate_user(self, user_id: int) -> UserInDB | None:
        db_user = await self.session.get(Db_User, user_id)
        if not db_user:
            return None
        db_user.is_active = False
        await self.session.flush()
        return UserInDB.model_validate(db_user)

    async def soft_delete_user(self, user_id: int) -> UserInDB | None:
        db_user = await self.session.get(Db_User, user_id)
        if not db_user:
            return None
        db_user.is_active = False
        db_user.deleted_at = datetime.now(UTC)
        await self.session.flush()
        return UserInDB.model_validate(db_user)

    async def restore_user(self, user_id: int) -> UserInDB | None:
        db_user = await self.session.get(Db_User, user_id)
        if not db_user:
            return None
        db_user.is_active = True
        db_user.deleted_at = None
        await self.session.flush()
        return UserInDB.model_validate(db_user)

    async def set_superuser(self, user_id: int) -> UserInDB | None:
        db_user = await self.session.get(Db_User, user_id)
        if not db_user:
            return None
        db_user.is_superuser = True
        await self.session.flush()
        return UserInDB.model_validate(db_user)

    async def unset_superuser(self, user_id: int) -> UserInDB | None:
        db_user = await self.session.get(Db_User, user_id)
        if not db_user:
            return None
        db_user.is_superuser = False
        await self.session.flush()
        return UserInDB.model_validate(db_user)

    # Query/Filter Methods
    async def get_all_users(
        self, offset: int = 0, limit: int = 50, is_active: bool | None = None
    ) -> list[UserInDB]:
        stmt = select(Db_User).offset(offset).limit(limit).order_by(Db_User.created_at)
        if is_active is not None:
            stmt = stmt.where(Db_User.is_active == is_active)
        result = await self.session.execute(stmt)
        return [UserInDB.model_validate(user) for user in result.scalars().all()]

    async def get_superusers(self, offset: int = 0, limit: int = 50) -> list[UserInDB]:
        stmt = select(Db_User).where(Db_User.is_superuser).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return [UserInDB.model_validate(user) for user in result.scalars().all()]

    async def get_soft_deleted_users(
        self, offset: int = 0, limit: int = 50
    ) -> list[UserInDB]:
        stmt = (
            select(Db_User)
            .where(Db_User.is_active.is_(False))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return [UserInDB.model_validate(user) for user in result.scalars().all()]

    async def get_users_by_filter(
        self, filters: dict, offset: int = 0, limit: int = 50
    ) -> list[UserInDB]:
        stmt = select(Db_User)
        for key, value in filters.items():
            if hasattr(Db_User, key):
                stmt = stmt.where(getattr(Db_User, key) == value)
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return [UserInDB.model_validate(user) for user in result.scalars().all()]

    # Utility Methods
    async def count_users(self, is_active: bool | None = None) -> int:
        stmt = select(func.count()).select_from(Db_User)
        if is_active is not None:
            stmt = stmt.where(Db_User.is_active == is_active)

        # Gunakan scalar_one() untuk mendapatkan hasil tunggal
        total_users = await self.session.scalar(stmt)
        return total_users or 0
