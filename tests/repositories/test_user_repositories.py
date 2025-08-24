"""
Unit test untuk UserRepo (repository layer).
Test CRUD, soft delete, restore, activate, deactivate, dan list.
"""

import app.models as models
import pytest
from app.database.repositories.repo_user import UserRepo
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_and_get_user(db_session: AsyncSession):
    repo = UserRepo()
    user = models.User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpw",
    )
    created = await repo.create(db_session, user)
    assert created.id is not None
    fetched = await repo.get_by_id(db_session, created.id)
    assert fetched.username == "testuser"


@pytest.mark.asyncio
async def test_update_user(db_session: AsyncSession):
    repo = UserRepo()
    user = models.User(
        username="updateuser",
        email="old@example.com",
        full_name="Old Name",
        hashed_password="pw",
    )
    created = await repo.create(db_session, user)
    created.email = "new@example.com"
    created.full_name = "New Name"
    updated = await repo.update(db_session, created)
    assert updated.email == "new@example.com"
    assert updated.full_name == "New Name"


@pytest.mark.asyncio
async def test_soft_delete_and_restore(db_session: AsyncSession):
    repo = UserRepo()
    user = models.User(
        username="softdel",
        email="soft@example.com",
        full_name="Soft Del",
        hashed_password="pw",
    )
    created = await repo.create(db_session, user)
    soft_deleted = await repo.soft_delete(db_session, created)
    assert soft_deleted.deleted_at is not None
    assert soft_deleted.is_active is False
    restored = await repo.restore(db_session, soft_deleted)
    assert restored.deleted_at is None
    assert restored.is_active is True


@pytest.mark.asyncio
async def test_activate_deactivate(db_session: AsyncSession):
    repo = UserRepo()
    user = models.User(
        username="statususer",
        email="status@example.com",
        full_name="Status User",
        hashed_password="pw",
        is_active=False,
    )
    created = await repo.create(db_session, user)
    activated = await repo.activate(db_session, created)
    assert activated.is_active is True
    deactivated = await repo.deactivate(db_session, activated)
    assert deactivated.is_active is False


@pytest.mark.asyncio
async def test_list_users(db_session: AsyncSession):
    repo = UserRepo()
    # Buat beberapa user
    for i in range(3):
        user = models.User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            full_name=f"User {i}",
            hashed_password="pw",
        )
        await repo.create(db_session, user)
    users = await repo.list_users(db_session)
    assert len(users) >= 3
