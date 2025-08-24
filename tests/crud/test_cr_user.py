"""
Unit tests for UserCRUD (schema response: UserInDB).
"""

import pytest
from app.crud.cr_user import UserCRUD
from app.schemas import UserInDB, UserUpdate
from app.services.hasher.implement import Argon2Hasher
from sqlalchemy import text


# Clean up users table before each test
@pytest.fixture(autouse=True)
async def cleanup_users_table(db_session):
    await db_session.execute(text("DELETE FROM users"))
    await db_session.commit()


@pytest.mark.asyncio
async def test_create_and_get_user(db_session):
    hasher = Argon2Hasher()
    user = await UserCRUD.create(
        db_session,
        username="testuser",
        email="testuser@example.com",
        full_name="Test User",
        hashed_password=hasher.hash("password123"),
    )
    assert isinstance(user, UserInDB)
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True
    fetched = await UserCRUD.get(db_session, str(user.id))
    assert fetched is not None
    assert fetched.username == "testuser"


@pytest.mark.asyncio
async def test_get_by_username_and_email(db_session):
    hasher = Argon2Hasher()
    user = await UserCRUD.create(
        db_session,
        username="user2",
        email="user2@example.com",
        full_name="User Two",
        hashed_password=hasher.hash("pass2"),
    )
    by_username = await UserCRUD.get_by_username(db_session, "user2")
    by_email = await UserCRUD.get_by_email(db_session, "user2@example.com")
    assert by_username is not None
    assert by_email is not None
    assert by_username.id == user.id
    assert by_email.id == user.id


@pytest.mark.asyncio
async def test_update_user(db_session):
    hasher = Argon2Hasher()
    user = await UserCRUD.create(
        db_session,
        username="user3",
        email="user3@example.com",
        full_name="User Three",
        hashed_password=hasher.hash("pass3"),
    )
    update_data = UserUpdate(email="newemail@example.com", full_name="User 3 Updated")
    updated = await UserCRUD.update(db_session, str(user.id), update_data)
    assert updated is not None
    if updated:
        assert updated.email == "newemail@example.com"
        assert updated.full_name == "User 3 Updated"


@pytest.mark.asyncio
async def test_delete_user(db_session):
    hasher = Argon2Hasher()
    user = await UserCRUD.create(
        db_session,
        username="user4",
        email="user4@example.com",
        full_name="User Four",
        hashed_password=hasher.hash("pass4"),
    )
    deleted = await UserCRUD.delete(db_session, str(user.id))
    assert deleted is True
    fetched = await UserCRUD.get(db_session, str(user.id))
    assert fetched is None


@pytest.mark.asyncio
async def test_soft_delete_user(db_session):
    hasher = Argon2Hasher()
    user = await UserCRUD.create(
        db_session,
        username="user5",
        email="user5@example.com",
        full_name="User Five",
        hashed_password=hasher.hash("pass5"),
    )
    soft_deleted = await UserCRUD.soft_delete(db_session, str(user.id))
    assert soft_deleted is not None
    if soft_deleted:
        assert soft_deleted.is_active is False
        assert soft_deleted.deleted_at is not None
