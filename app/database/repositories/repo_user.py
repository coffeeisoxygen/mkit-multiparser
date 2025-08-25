import uuid
from datetime import UTC, datetime

from app.database.repositories.intf_user import IUserRepository
from app.models.db_user import User
from app.schemas.user.sch_user import UserCreate, UserInDB, UserUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_user_with_id(self, user_id: uuid.UUID) -> UserInDB | None:
        user = await self.session.get(User, str(user_id))
        return UserInDB.model_validate(user) if user else None

    async def get_user_with_username(self, username: str) -> UserInDB | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserInDB.model_validate(user) if user else None

    async def get_user_with_email(self, email: str) -> UserInDB | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserInDB.model_validate(user) if user else None

    async def get_all_users(
        self, offset: int = 0, limit: int = 50, is_active: bool | None = None
    ) -> list[UserInDB]:
        stmt = select(User).offset(offset).limit(limit).order_by(User.created_at)
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return [UserInDB.model_validate(u) for u in users]

    async def create_user(self, user_in: UserCreate) -> UserInDB:
        # Use Pydantic's model_dump() to convert the input schema to a dictionary
        # This eliminates the manual mapping.
        user_data = user_in.model_dump()
        db_user = User(**user_data)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return UserInDB.model_validate(db_user)

    async def update_user(
        self, user_id: uuid.UUID, user_in: UserUpdate
    ) -> UserInDB | None:
        db_user = await self.session.get(User, str(user_id))
        if not db_user:
            return None

        # Use model_dump(exclude_unset=True) to get a dict of only the fields provided
        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        await self.session.commit()
        await self.session.refresh(db_user)
        return UserInDB.model_validate(db_user)

    async def soft_delete_user(self, user_id: uuid.UUID) -> UserInDB | None:
        db_user = await self.session.get(User, str(user_id))
        if not db_user:
            return None

        db_user.is_active = False
        db_user.deleted_at = datetime.now(UTC)

        await self.session.commit()
        await self.session.refresh(db_user)
        return UserInDB.model_validate(db_user)

    async def restore_user(self, user_id: uuid.UUID) -> UserInDB | None:
        db_user = await self.session.get(User, str(user_id))
        if not db_user:
            return None

        db_user.is_active = True
        db_user.deleted_at = None

        await self.session.commit()
        await self.session.refresh(db_user)
        return UserInDB.model_validate(db_user)
