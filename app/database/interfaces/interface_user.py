import uuid
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

import app.models as models


class IUserRepo(Protocol):
    """Interface untuk operasi User di database."""

    async def create(self, db: AsyncSession, user: models.User) -> models.User: ...
    async def update(self, db: AsyncSession, user: models.User) -> models.User: ...
    async def delete(self, db: AsyncSession, user: models.User) -> None: ...
    async def soft_delete(self, db: AsyncSession, user: models.User) -> models.User: ...
    async def restore(self, db: AsyncSession, user: models.User) -> models.User: ...
    async def activate(self, db: AsyncSession, user: models.User) -> models.User: ...
    async def deactivate(self, db: AsyncSession, user: models.User) -> models.User: ...

    async def get_by_id(
        self, db: AsyncSession, user_id: uuid.UUID
    ) -> models.User | None: ...

    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> models.User | None: ...

    async def list_users(
        self,
        db: AsyncSession,
        *,
        limit: int = 50,
        offset: int = 0,
        is_active: bool | None = None,
    ) -> list[models.User]: ...
