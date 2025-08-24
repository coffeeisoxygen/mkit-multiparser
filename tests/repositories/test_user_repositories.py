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
    fetched = await repo.get_by_id(db_session, created.id)  # type: ignore
    assert fetched.username == "testuser"  # type: ignore


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


@pytest.mark.asyncio
async def test_list_users_limit_offset(db_session: AsyncSession):
    repo = UserRepo()
    # Buat 5 user
    for i in range(5):
        user = models.User(
            username=f"limituser{i}",
            email=f"limituser{i}@example.com",
            full_name=f"Limit User {i}",
            hashed_password="pw",
        )
        await repo.create(db_session, user)
    # Ambil 2 user pertama
    users_limit_2 = await repo.list_users(db_session, limit=2)
    assert len(users_limit_2) == 2
    # Ambil user ke-3 dan ke-4
    users_offset_2 = await repo.list_users(db_session, limit=2, offset=2)
    assert len(users_offset_2) == 2
    # Pastikan urutan offset benar
    assert users_offset_2[0].username == "limituser2"
    assert users_offset_2[1].username == "limituser3"


@pytest.mark.asyncio
async def test_list_users_limit_offset_is_active(db_session: AsyncSession):
    repo = UserRepo()
    # Buat 3 user aktif, 2 user nonaktif
    for i in range(3):
        user = models.User(
            username=f"activepag{i}",
            email=f"activepag{i}@example.com",
            full_name=f"Active Pag {i}",
            hashed_password="pw",
            is_active=True,
        )
        await repo.create(db_session, user)
    for i in range(2):
        user = models.User(
            username=f"inactivepag{i}",
            email=f"inactivepag{i}@example.com",
            full_name=f"Inactive Pag {i}",
            hashed_password="pw",
            is_active=False,
        )
        await repo.create(db_session, user)
    # Ambil 2 user aktif pertama
    users_active = await repo.list_users(db_session, limit=2, is_active=True)
    assert len(users_active) == 2
    assert all(u.is_active for u in users_active)
    # Ambil 1 user nonaktif pertama
    users_inactive = await repo.list_users(db_session, limit=1, is_active=False)
    assert len(users_inactive) == 1
    assert all(not u.is_active for u in users_inactive)
