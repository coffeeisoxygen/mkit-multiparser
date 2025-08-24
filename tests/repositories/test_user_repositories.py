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


@pytest.mark.asyncio
async def test_create_duplicate_user_should_fail(db_session: AsyncSession):
    repo = UserRepo()
    user1 = models.User(
        username="dupeuser",
        email="dupe@example.com",
        full_name="Dupe User",
        hashed_password="pw",
    )
    user2 = models.User(
        username="dupeuser",
        email="dupe@example.com",
        full_name="Dupe User",
        hashed_password="pw",
    )
    await repo.create(db_session, user1)
    with pytest.raises(Exception):
        await repo.create(db_session, user2)


@pytest.mark.asyncio
async def test_create_user_with_empty_fields_should_fail(db_session: AsyncSession):
    repo = UserRepo()
    user = models.User(
        username=None,
        email=None,
        full_name=None,
        hashed_password="pw",
    )
    with pytest.raises(Exception):
        await repo.create(db_session, user)


@pytest.mark.asyncio
async def test_soft_delete_already_deleted_user(db_session: AsyncSession):
    repo = UserRepo()
    user = models.User(
        username="alreadydeleted",
        email="alreadydeleted@example.com",
        full_name="Already Deleted",
        hashed_password="pw",
    )
    created = await repo.create(db_session, user)
    await repo.soft_delete(db_session, created)
    # Soft delete lagi
    result = await repo.soft_delete(db_session, created)
    assert result.deleted_at is not None
    assert result.is_active is False


@pytest.mark.asyncio
async def test_restore_user_not_deleted(db_session: AsyncSession):
    repo = UserRepo()
    user = models.User(
        username="notdeleted",
        email="notdeleted@example.com",
        full_name="Not Deleted",
        hashed_password="pw",
    )
    created = await repo.create(db_session, user)
    # Restore user yang belum dihapus
    result = await repo.restore(db_session, created)
    assert result.deleted_at is None
    assert result.is_active is True


@pytest.mark.asyncio
async def test_list_users_active_only(db_session: AsyncSession):
    repo = UserRepo()
    # Buat user aktif dan nonaktif
    active_user = models.User(
        username="activeuser",
        email="active@example.com",
        full_name="Active User",
        hashed_password="pw",
        is_active=True,
    )
    inactive_user = models.User(
        username="inactiveuser",
        email="inactive@example.com",
        full_name="Inactive User",
        hashed_password="pw",
        is_active=False,
    )
    await repo.create(db_session, active_user)
    await repo.create(db_session, inactive_user)
    users = await repo.list_users(db_session, is_active=True)
    assert all(u.is_active for u in users)
