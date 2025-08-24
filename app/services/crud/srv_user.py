import uuid

import app.models as models
from app.database.interfaces.interface_user import IUserRepo
from app.exception import (
    UserCreationError,
    UserDuplicateError,
    UserNotFoundError,
    UserPasswordError,
)
from app.schemas.user.sch_user import (
    UserCreate,
    UserRead,
    UserUpdate,
    UserUpdatePassword,
)
from app.services.hasher.implement import Argon2Hasher
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, repo: IUserRepo):
        self.repo = repo
        self.hasher = Argon2Hasher()

    # --- Create ---
    async def create_user(self, db: AsyncSession, data: UserCreate) -> UserRead:
        if await self.repo.get_by_username(db, data.username):
            raise UserDuplicateError(context={"username": data.username})

        user = models.User(
            username=data.username,
            email=data.email,
            full_name=data.full_name,
            hashed_password=self.hasher.hash(data.password),
        )

        try:
            created = await self.repo.create(db, user)
            return UserRead.model_validate(created)
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise UserCreationError(context={"username": data.username}) from e

    # --- Read ---
    async def get_user(self, db: AsyncSession, user_id: uuid.UUID) -> UserRead:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(context={"user_id": str(user_id)})
        return UserRead.model_validate(user)

    # --- Update Profile ---
    async def update_profile(
        self, db: AsyncSession, user_id: uuid.UUID, data: UserUpdate
    ) -> UserRead:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(context={"user_id": str(user_id)})

        if data.email is not None:
            user.email = data.email
        if data.full_name is not None:
            user.full_name = data.full_name

        updated = await self.repo.update(db, user)
        await db.refresh(updated)
        return UserRead.model_validate(updated)

    # --- Update Password ---
    async def update_password(
        self, db: AsyncSession, user_id: uuid.UUID, data: UserUpdatePassword
    ) -> UserRead:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(context={"user_id": str(user_id)})

        if not self.hasher.verify(data.old_password, user.hashed_password):
            raise UserPasswordError(message="Old password is incorrect")

        if data.new_password != data.confirm_password:
            raise UserPasswordError(message="New password confirmation mismatch")

        user.hashed_password = self.hasher.hash(data.new_password)
        updated = await self.repo.update(db, user)
        await db.refresh(updated)
        return UserRead.model_validate(updated)

    # --- Soft Delete / Activate / Deactivate ---
    async def soft_delete(self, db: AsyncSession, user_id: uuid.UUID) -> UserRead:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(context={"user_id": str(user_id)})
        updated = await self.repo.soft_delete(db, user)
        await db.refresh(updated)
        return UserRead.model_validate(updated)

    async def restore(self, db: AsyncSession, user_id: uuid.UUID) -> UserRead:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(context={"user_id": str(user_id)})
        updated = await self.repo.restore(db, user)
        await db.refresh(updated)
        return UserRead.model_validate(updated)

    async def activate(self, db: AsyncSession, user_id: uuid.UUID) -> UserRead:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(context={"user_id": str(user_id)})
        updated = await self.repo.activate(db, user)
        await db.refresh(updated)
        return UserRead.model_validate(updated)

    async def deactivate(self, db: AsyncSession, user_id: uuid.UUID) -> UserRead:
        user = await self.repo.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(context={"user_id": str(user_id)})
        updated = await self.repo.deactivate(db, user)
        await db.refresh(updated)
        return UserRead.model_validate(updated)
