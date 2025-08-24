"""class crud methods for user."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.models as models
from app.exception import UserDuplicateError, UserNotFoundError
from app.schemas import UserCreate, UserRead
from app.services.hasher.implement import Argon2Hasher


async def get_user(db_session: AsyncSession, user_id: uuid.UUID) -> UserRead:
    """Get user by ID."""
    result = await db_session.execute(
        select(models.User).where(models.User.id == str(user_id))
    )
    user = result.scalars().first()
    if not user:
        raise UserNotFoundError(context={"user_id": user_id})
    return UserRead.model_validate(user)


async def get_user_by_username(
    db_session: AsyncSession, username: str
) -> UserRead | None:
    """Get user by username."""
    result = await db_session.execute(
        select(models.User).where(models.User.username == username)
    )
    user = result.scalars().first()
    if not user:
        return None
    return UserRead.model_validate(user)


async def create_user(db_session: AsyncSession, user_data: UserCreate) -> UserRead:
    """Create a new user.

    Raises:
        UserDuplicateError: If user with the same username already exists.
    """
    # Check if username already exists
    result = await db_session.execute(
        select(models.User).where(models.User.username == user_data.username)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise UserDuplicateError(context={"username": user_data.username})

    hasher = Argon2Hasher()
    hashed_pw = hasher.hash(user_data.password)
    user_dict = user_data.model_dump(exclude={"password"})
    user = models.User(**user_dict, hashed_password=hashed_pw)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return UserRead.model_validate(user)
