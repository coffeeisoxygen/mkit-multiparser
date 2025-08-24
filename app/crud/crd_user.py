"""class crud methods for user."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.models as models
from app.exception import UserDuplicateError, UserNotFoundError, UserPasswordError
from app.schemas import UserCreate, UserRead
from app.schemas.user.sch_user import UserUpdate, UserUpdatePassword
from app.services.hasher.implement import Argon2Hasher


async def get_user_or_404(db_session: AsyncSession, user_id: uuid.UUID) -> models.User:
    """Get user by ID or raise UserNotFoundError."""
    user = await db_session.get(models.User, str(user_id))
    if not user:
        raise UserNotFoundError(context={"user_id": user_id})
    return user


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


async def update_user_profile(
    db_session: AsyncSession, user_id: uuid.UUID, user_data: UserUpdate
) -> UserRead:
    """Update user profile (email, full_name)."""
    user = await get_user_or_404(db_session, user_id)

    # Update only allowed fields
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.full_name is not None:
        user.full_name = user_data.full_name

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return UserRead.model_validate(user)


async def update_user_password(
    db_session: AsyncSession, user_id: uuid.UUID, user_data: UserUpdatePassword
) -> UserRead:
    """Update user password with validation."""
    user = await get_user_or_404(db_session, user_id)

    hasher = Argon2Hasher()
    if not hasher.verify(user_data.old_password, user.hashed_password):
        raise UserPasswordError(
            message="Old password is incorrect", context={"user_id": user_id}
        )
    # Validate new password confirmation
    if user_data.new_password != user_data.confirm_password:
        raise UserPasswordError(
            message="New password and confirmation do not match",
            context={"user_id": user_id},
        )

    user.hashed_password = hasher.hash(user_data.new_password)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return UserRead.model_validate(user)


async def soft_delete_user(db_session: AsyncSession, user_id: uuid.UUID) -> UserRead:
    """Soft delete a user by ID."""
    user = await get_user_or_404(db_session, user_id)
    user.is_active = False
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return UserRead.model_validate(user)
