"""class crud methods for user."""

import uuid
from datetime import UTC, datetime

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.models as models
from app.exception import UserDuplicateError, UserNotFoundError, UserPasswordError
from app.schemas import UserCreate, UserRead
from app.schemas.user.sch_user import UserUpdate, UserUpdatePassword
from app.services.hasher.implement import Argon2Hasher


async def get_user_or_404(db_session: AsyncSession, user_id: uuid.UUID) -> models.User:
    """Get user by ID (not soft deleted) or raise UserNotFoundError."""
    with logger.contextualize(user_id=str(user_id)):
        result = await db_session.execute(
            select(models.User)
            .where(models.User.id == str(user_id))
            .where(models.User.deleted_at.is_(None))
        )
        user = result.scalars().first()
        if not user:
            logger.warning("User not found")
            raise UserNotFoundError(context={"user_id": user_id})
        logger.info("User found")
        return user


async def get_user(db_session: AsyncSession, user_id: uuid.UUID) -> UserRead:
    """Get user by ID (not soft deleted)."""
    with logger.contextualize(user_id=str(user_id)):
        result = await db_session.execute(
            select(models.User)
            .where(models.User.id == str(user_id))
            .where(models.User.deleted_at.is_(None))
        )
        user = result.scalars().first()
        if not user:
            logger.warning("User not found")
            raise UserNotFoundError(context={"user_id": user_id})
        logger.info("User found")
        return UserRead.model_validate(user)


async def get_user_by_username(
    db_session: AsyncSession, username: str
) -> UserRead | None:
    """Get user by username (not soft deleted)."""
    with logger.contextualize(username=username):
        result = await db_session.execute(
            select(models.User)
            .where(models.User.username == username)
            .where(models.User.deleted_at.is_(None))
        )
        user = result.scalars().first()
        if not user:
            logger.warning("User not found")
            return None
        logger.info("User found")
        return UserRead.model_validate(user)


async def get_user_list(db_session: AsyncSession) -> list[UserRead]:
    """Get list of users (not soft deleted)."""
    logger.info("Fetching user list")
    result = await db_session.execute(
        select(models.User).where(models.User.deleted_at.is_(None))
    )
    users = result.scalars().all()
    logger.info(f"Found {len(users)} users")
    return [UserRead.model_validate(user) for user in users]


async def create_user(db_session: AsyncSession, user_data: UserCreate) -> UserRead:
    """Create a new user.

    Raises:
        UserDuplicateError: If user with the same username already exists (not soft deleted).
    """
    with logger.contextualize(username=user_data.username, email=user_data.email):
        result = await db_session.execute(
            select(models.User)
            .where(models.User.username == user_data.username)
            .where(models.User.deleted_at.is_(None))
        )
        existing_user = result.scalars().first()
        if existing_user:
            logger.warning("Duplicate user")
            raise UserDuplicateError(context={"username": user_data.username})

        hasher = Argon2Hasher()
        hashed_pw = hasher.hash(user_data.password)
        user_dict = user_data.model_dump(exclude={"password"})
        user = models.User(**user_dict, hashed_password=hashed_pw)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        logger.info("User created")
        return UserRead.model_validate(user)


async def update_user_profile(
    db_session: AsyncSession, user_id: uuid.UUID, user_data: UserUpdate
) -> UserRead:
    """Update user profile (email, full_name) if not soft deleted."""
    with logger.contextualize(user_id=str(user_id)):
        user = await get_user_or_404(db_session, user_id)

        # Update only allowed fields
        if user_data.email is not None:
            user.email = user_data.email
        if user_data.full_name is not None:
            user.full_name = user_data.full_name

        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        logger.info("User profile updated")
        return UserRead.model_validate(user)


async def update_user_password(
    db_session: AsyncSession, user_id: uuid.UUID, user_data: UserUpdatePassword
) -> UserRead:
    """Update user password with validation if not soft deleted."""
    with logger.contextualize(user_id=str(user_id)):
        user = await get_user_or_404(db_session, user_id)

        hasher = Argon2Hasher()
        if not hasher.verify(user_data.old_password, user.hashed_password):
            logger.warning("Old password incorrect")
            raise UserPasswordError(
                message="Old password is incorrect", context={"user_id": user_id}
            )
        # Validate new password confirmation
        if user_data.new_password != user_data.confirm_password:
            logger.warning("Password confirmation mismatch")
            raise UserPasswordError(
                message="New password and confirmation do not match",
                context={"user_id": user_id},
            )

        user.hashed_password = hasher.hash(user_data.new_password)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        logger.info("User password updated")
        return UserRead.model_validate(user)


async def soft_delete_user(db_session: AsyncSession, user_id: uuid.UUID) -> UserRead:
    """Soft delete a user by ID (set deleted_at and is_active=False)."""
    with logger.contextualize(user_id=str(user_id)):
        user = await get_user_or_404(db_session, user_id)

        user.deleted_at = datetime.now(UTC)
        user.is_active = False
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        logger.info("User soft deleted")
        return UserRead.model_validate(user)


async def activate_user(db_session: AsyncSession, user_id: uuid.UUID) -> UserRead:
    """Activate user (set is_active=True) if not soft deleted."""
    with logger.contextualize(user_id=str(user_id)):
        user = await get_user_or_404(db_session, user_id)
        user.is_active = True
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        logger.info("User activated")
        return UserRead.model_validate(user)


async def deactivate_user(db_session: AsyncSession, user_id: uuid.UUID) -> UserRead:
    """Deactivate user (set is_active=False) if not soft deleted."""
    with logger.contextualize(user_id=str(user_id)):
        user = await get_user_or_404(db_session, user_id)
        user.is_active = False
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        logger.info("User deactivated")
        return UserRead.model_validate(user)


async def restore_user(db_session: AsyncSession, user_id: uuid.UUID) -> UserRead:
    """Restore user from soft delete (set deleted_at=None, is_active=True)."""
    with logger.contextualize(user_id=str(user_id)):
        result = await db_session.execute(
            select(models.User)
            .where(models.User.id == str(user_id))
            .where(models.User.deleted_at.is_not(None))
        )
        user = result.scalars().first()
        if not user:
            logger.warning("User not found for restore")
            raise UserNotFoundError(context={"user_id": user_id})
        user.deleted_at = None
        user.is_active = True
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        logger.info("User restored from soft delete")
        return UserRead.model_validate(user)
