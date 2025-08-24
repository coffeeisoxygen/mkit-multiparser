"""CRUD operations for User model. Only handles persistence, no business logic."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserInDB, UserUpdate


class UserCRUD:
    """CRUD class for User. All business logic/validation should be in service layer."""

    @staticmethod
    async def create(
        session: AsyncSession,
        *,
        username: str,
        email: str,
        full_name: str,
        hashed_password: str,
    ) -> "UserInDB":
        """Create new user and return UserInDB schema."""
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return UserInDB.model_validate(user)

    @staticmethod
    async def get(session: AsyncSession, user_id: str) -> "UserInDB | None":
        """Get user by ID and return UserInDB schema or None."""
        user = await session.get(User, user_id)
        if not user:
            return None
        return UserInDB.model_validate(user)

    @staticmethod
    async def get_by_username(
        session: AsyncSession, username: str
    ) -> "UserInDB | None":
        """Get user by username and return UserInDB schema or None."""
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserInDB.model_validate(user)

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> "UserInDB | None":
        """Get user by email and return UserInDB schema or None."""
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserInDB.model_validate(user)

    @staticmethod
    async def get_all(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 50,
        is_active: bool | None = None,
    ) -> "list[UserInDB]":
        """Get all users with optional filtering, return list of UserInDB."""
        stmt = select(User).offset(offset).limit(limit).order_by(User.created_at)
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)
        result = await session.execute(stmt)
        users = list(result.scalars().all())
        return [UserInDB.model_validate(u) for u in users]

    @staticmethod
    async def update(
        session: AsyncSession, user_id: str, user_data: UserUpdate
    ) -> "UserInDB | None":
        """Update user and return UserInDB schema or None."""
        user = await session.get(User, user_id)
        if not user:
            return None
        update_dict = user_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(user, field, value)
        await session.commit()
        await session.refresh(user)
        return UserInDB.model_validate(user)

    @staticmethod
    async def delete(session: AsyncSession, user_id: str) -> bool:
        """Delete user. Return True if deleted, False if not found."""
        user = await session.get(User, user_id)
        if not user:
            return False
        await session.delete(user)
        await session.commit()
        return True

    @staticmethod
    async def soft_delete(session: AsyncSession, user_id: str) -> "UserInDB | None":
        """Soft delete user and return UserInDB schema or None."""
        user = await session.get(User, user_id)
        if not user:
            return None
        user.is_active = False
        user.deleted_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(user)
        return UserInDB.model_validate(user)
