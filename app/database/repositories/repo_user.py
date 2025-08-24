import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.models as models
from app.database.interfaces.interface_user import IUserRepo


class UserRepo(IUserRepo):
    """Implementasi repository untuk User (SQLAlchemy)."""

    # --- CRUD ---
    async def create(self, db: AsyncSession, user: models.User) -> models.User:
        db.add(user)
        await db.flush()
        return user

    async def update(self, db: AsyncSession, user: models.User) -> models.User:
        await db.flush()
        return user

    async def delete(self, db: AsyncSession, user: models.User) -> None:
        await db.delete(user)
        await db.flush()

    # --- Retrieval ---
    async def get_by_id(
        self, db: AsyncSession, user_id: uuid.UUID
    ) -> models.User | None:
        stmt = select(models.User).where(models.User.id == str(user_id))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> models.User | None:
        stmt = select(models.User).where(models.User.username == username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_users(
        self,
        db: AsyncSession,
        *,
        limit: int = 50,
        offset: int = 0,
        is_active: bool | None = None,
    ) -> list[models.User]:
        stmt = (
            select(models.User)
            .order_by(models.User.username)
            .offset(offset)
            .limit(limit)
        )

        if is_active is not None:
            stmt = stmt.where(models.User.is_active == is_active)

        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def restore(self, db: AsyncSession, user: models.User) -> models.User:
        user.deleted_at = None
        user.is_active = True
        await db.flush()
        return user

    async def activate(self, db: AsyncSession, user: models.User) -> models.User:
        user.is_active = True
        await db.flush()
        return user

    async def deactivate(self, db: AsyncSession, user: models.User) -> models.User:
        user.is_active = False
        await db.flush()
        return user

    async def soft_delete(self, db: AsyncSession, user: models.User) -> models.User:
        user.deleted_at = datetime.now(UTC)
        user.is_active = False
        await db.flush()
        return user
