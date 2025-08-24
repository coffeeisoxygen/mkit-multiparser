# crud/user.py

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate, UserUpdate


class UserCRUD:
    @staticmethod
    async def create(session: AsyncSession, user_data: UserCreate) -> User:
        """Create new user."""
        user = User(**user_data.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get(session: AsyncSession, user_id: str) -> User | None:
        """Get user by ID."""
        return await session.get(User, user_id)

    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> User | None:
        """Get user by username."""
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        """Get user by email."""
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 50,
        is_active: bool | None = None,
    ) -> list[User]:
        """Get all users with filtering."""
        stmt = select(User).offset(offset).limit(limit).order_by(User.created_at)

        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)

        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def update(
        session: AsyncSession, user_id: str, user_data: UserUpdate
    ) -> User | None:
        """Update user."""
        user = await session.get(User, user_id)
        if not user:
            return None

        update_dict = user_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(user, field, value)

        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete(session: AsyncSession, user_id: str) -> bool:
        """Delete user."""
        user = await session.get(User, user_id)
        if not user:
            return False

        await session.delete(user)
        await session.commit()
        return True

    @staticmethod
    async def soft_delete(session: AsyncSession, user_id: str) -> User | None:
        """Soft delete user."""
        user = await session.get(User, user_id)
        if not user:
            return None

        user.is_active = False
        user.deleted_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(user)
        return user
