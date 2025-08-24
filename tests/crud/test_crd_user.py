"""Test CRUD user: get by id and username."""

import uuid

import pytest
from app.crud.crd_user import get_user, get_user_by_username
from app.models import User
from sqlalchemy import delete


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
    with pytest.raises(Exception):
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
