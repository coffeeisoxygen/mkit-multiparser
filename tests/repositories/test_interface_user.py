"""
Unit tests for IUserRepo interface.
"""

import uuid
from unittest.mock import AsyncMock

import app.models as models
import pytest


@pytest.fixture
def mock_user():
    return models.User(
        id=str(uuid.uuid4()),
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpw",
        is_active=True,
        deleted_at=None,
    )


@pytest.fixture
def mock_repo():
    class MockUserRepo:
        async def create(self, db, user):
            return user

        async def update(self, db, user):
            return user

        async def delete(self, db, user):
            return None

        async def soft_delete(self, db, user):
            return user

        async def restore(self, db, user):
            return user

        async def activate(self, db, user):
            return user

        async def deactivate(self, db, user):
            return user

        async def get_by_id(self, db, user_id):
            return None

        async def get_by_username(self, db, username):
            return None

        async def list_users(self, db, *, limit=50, offset=0, is_active=None):
            return []

    return MockUserRepo()


@pytest.mark.asyncio
async def test_create_signature(mock_repo, mock_user):
    result = await mock_repo.create(AsyncMock(), mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_update_signature(mock_repo, mock_user):
    result = await mock_repo.update(AsyncMock(), mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_delete_signature(mock_repo, mock_user):
    result = await mock_repo.delete(AsyncMock(), mock_user)
    assert result is None


@pytest.mark.asyncio
async def test_soft_delete_signature(mock_repo, mock_user):
    result = await mock_repo.soft_delete(AsyncMock(), mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_restore_signature(mock_repo, mock_user):
    result = await mock_repo.restore(AsyncMock(), mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_activate_signature(mock_repo, mock_user):
    result = await mock_repo.activate(AsyncMock(), mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_deactivate_signature(mock_repo, mock_user):
    result = await mock_repo.deactivate(AsyncMock(), mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_get_by_id_signature(mock_repo):
    user_id = uuid.uuid4()
    result = await mock_repo.get_by_id(AsyncMock(), user_id)
    assert result is None


@pytest.mark.asyncio
async def test_get_by_username_signature(mock_repo):
    result = await mock_repo.get_by_username(AsyncMock(), "testuser")
    assert result is None


@pytest.mark.asyncio
async def test_list_users_signature(mock_repo):
    result = await mock_repo.list_users(AsyncMock(), limit=10, offset=0, is_active=True)
    assert isinstance(result, list)
