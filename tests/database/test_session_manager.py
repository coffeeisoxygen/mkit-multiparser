"""
Integration tests for DatabaseSessionManager and session helpers.

These tests cover normal and error scenarios for session management.
"""

import pytest
from app.database.core.session import (
    get_db_session_auto_commit,
    get_db_session_manual_commit,
)
from app.exception import InternalServiceError
from app.models import User
from sqlalchemy import delete


class SimulatedSessionError(Exception):
    """Custom exception for simulating session errors in tests."""


@pytest.mark.asyncio
async def test_manual_commit_success(db_session):
    """Test manual commit: user should be persisted."""
    # Clean up user table before test

    await db_session.execute(delete(User))
    await db_session.commit()
    user = User(
        username="sessiontest",
        email="sessiontest@example.com",
        full_name="Session Test",
        hashed_password="pw",
    )
    async with get_db_session_manual_commit() as session:
        session.add(user)
        await session.commit()
        result = await session.get(User, user.id)
        assert result is not None
        assert result.username == "sessiontest"


@pytest.mark.asyncio
async def test_manual_commit_rollback_on_error(db_session):
    """Test rollback on error: user should not be persisted."""

    await db_session.execute(delete(User))
    await db_session.commit()
    user = User(
        username="rollbacktest",
        email="rollbacktest@example.com",
        full_name="Rollback Test",
        hashed_password="pw",
    )

    def raise_simulated_error():
        raise SimulatedSessionError("Simulated error")

    try:
        async with get_db_session_manual_commit() as session:
            session.add(user)
            raise_simulated_error()
    except InternalServiceError:
        pass
    except SimulatedSessionError:
        pass
    async with get_db_session_manual_commit() as session:
        result = await session.get(User, user.id)
        assert result is None


@pytest.mark.asyncio
async def test_auto_commit_success(db_session):
    """Test auto commit: user should be persisted."""

    await db_session.execute(delete(User))
    await db_session.commit()
    user = User(
        username="autocommittest",
        email="autocommit@example.com",
        full_name="Auto Commit Test",
        hashed_password="pw",
    )
    async with get_db_session_auto_commit() as session:
        session.add(user)
    async with get_db_session_manual_commit() as session:
        result = await session.get(User, user.id)
        assert result is not None
        assert result.username == "autocommittest"


@pytest.mark.asyncio
async def test_auto_commit_rollback_on_error(db_session):
    """Test auto commit rollback on error: user should not be persisted."""

    await db_session.execute(delete(User))
    await db_session.commit()
    user = User(
        username="autocommitfail",
        email="autocommitfail@example.com",
        full_name="Auto Commit Fail",
        hashed_password="pw",
    )

    def raise_simulated_error():
        raise SimulatedSessionError("Simulated error")

    try:
        async with get_db_session_auto_commit() as session:
            session.add(user)
            raise_simulated_error()
    except InternalServiceError:
        pass
    except SimulatedSessionError:
        pass
    async with get_db_session_manual_commit() as session:
        result = await session.get(User, user.id)
        assert result is None
