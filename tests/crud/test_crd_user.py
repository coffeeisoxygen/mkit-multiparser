"""Test CRUD user: get by id and username."""

# pyright: reportOptionalMemberAccess = false
import uuid

import pytest
from app.crud.crd_user import create_user, get_user, get_user_by_username
from app.exception import UserDuplicateError, UserNotFoundError
from app.models import User
from app.schemas import UserCreate
from app.services.hasher.implement import Argon2Hasher
from sqlalchemy import delete


@pytest.mark.asyncio
async def test_create_user_success(db_session):
    # Cleanup: delete all users
    await db_session.execute(delete(User))
    await db_session.commit()

    # Arrange
    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        full_name="New User",
        password="mysecretpw",
    )

    # Act
    result = await create_user(db_session, user_data)

    # Assert
    assert result.username == "newuser"
    assert result.email == "newuser@example.com"
    assert result.full_name == "New User"
    assert result.id is not None

    # Check password is hashed in DB
    db_user = await db_session.get(User, str(result.id))
    hasher = Argon2Hasher()
    assert hasher.verify("mysecretpw", db_user.hashed_password)


@pytest.mark.asyncio
async def test_create_user_duplicate(db_session):
    # Cleanup: delete all users
    await db_session.execute(delete(User))
    await db_session.commit()

    # Arrange
    user_data = UserCreate(
        username="dupeuser",
        email="dupeuser@example.com",
        full_name="Dupe User",
        password="pw1",
    )
    await create_user(db_session, user_data)

    # Act & Assert
    with pytest.raises(UserDuplicateError):
        await create_user(db_session, user_data)


@pytest.mark.asyncio
async def test_get_user_found(db_session):
    # Cleanup: delete all users
    await db_session.execute(delete(User))
    await db_session.commit()

    # Arrange: create user
    user = User(
        id=str(uuid.uuid4()),
        username="testuser",
        email="testuser@example.com",
        full_name="Test User",
        hashed_password="hashedpw",
        is_superuser=True,
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Act
    result = await get_user(db_session, uuid.UUID(user.id))

    # Assert
    assert result.username == "testuser"
    assert result.email == "testuser@example.com"
    assert result.full_name == "Test User"
    assert result.id == uuid.UUID(user.id)


@pytest.mark.asyncio
async def test_get_user_not_found(db_session):
    # Act & Assert
    with pytest.raises(UserNotFoundError):
        await get_user(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_get_user_by_username_found(db_session):
    # Cleanup: delete all users
    await db_session.execute(delete(User))
    await db_session.commit()

    # Arrange: create user
    user = User(
        id=str(uuid.uuid4()),
        username="user2",
        email="user2@example.com",
        full_name="User Two",
        hashed_password="hashedpw2",
        is_superuser=False,
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Act
    result = await get_user_by_username(db_session, "user2")

    # Assert
    assert result.username == "user2"
    assert result.email == "user2@example.com"
    assert result.full_name == "User Two"
    assert result.id == uuid.UUID(user.id)


@pytest.mark.asyncio
async def test_get_user_by_username_not_found(db_session):
    # Act
    result = await get_user_by_username(db_session, "notfound")
    # Assert
    assert result is None
