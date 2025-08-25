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
        if not user:
            return None
        return UserInDB.model_validate(user)

    async def get_user_with_username(self, username: str) -> UserInDB | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserInDB.model_validate(user)

    async def get_user_with_email(self, email: str) -> UserInDB | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserInDB.model_validate(user)

    async def get_all_users(
        self, offset: int = 0, limit: int = 50, is_active: bool | None = None
    ) -> list[UserInDB]:
        stmt = select(User).offset(offset).limit(limit).order_by(User.created_at)
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return [UserInDB.model_validate(u) for u in users]

    async def create_user(self, user_in: UserCreate) -> UserInDB | None:
        db_user = User(**user_in.model_dump())
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
        db_user.deleted_at = datetime.now(
            UTC
        )  # Corrected to UTC based on our previous discussion

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
