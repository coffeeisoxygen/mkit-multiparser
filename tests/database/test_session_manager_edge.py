"""
Edge test cases for DatabaseSessionManager (error, monkeypatch, rollback).

These tests simulate error scenarios for session manager internals.
"""

import app.database.core.session as session_mod
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_engine_not_initialized(monkeypatch):
    """Test error when engine is None."""
    manager = session_mod.DatabaseSessionManager("sqlite+aiosqlite:///:memory:")
    manager.engine = None
    with pytest.raises(session_mod.InternalServiceError):
        async with manager.connect():
            pass


@pytest.mark.asyncio
async def test_sessionmaker_none(monkeypatch):
    """Test error when sessionmaker is None."""
    manager = session_mod.DatabaseSessionManager("sqlite+aiosqlite:///:memory:")
    manager._sessionmaker = None
    with pytest.raises(session_mod.InternalServiceError):
        async with manager.session():
            pass


@pytest.mark.asyncio
async def test_connect_raises_sqlalchemy_error(monkeypatch):
    """Test error raised in connect context manager."""
    manager = session_mod.DatabaseSessionManager("sqlite+aiosqlite:///:memory:")

    class FakeConnect:
        async def __aenter__(self):
            raise session_mod.SQLAlchemyError("Simulated connect error")

        async def __aexit__(self, exc_type, exc, tb):
            return None

    # Patch engine.connect to return FakeConnect instance
    def fake_connect(self, *args, **kwargs):
        return FakeConnect()

    monkeypatch.setattr(type(manager.engine), "connect", fake_connect)
    with pytest.raises(session_mod.InternalServiceError):
        async with manager.connect():
            pass


@pytest.mark.asyncio
async def test_session_raises_sqlalchemy_error(monkeypatch):
    """Test error raised in session context manager."""
    manager = session_mod.DatabaseSessionManager("sqlite+aiosqlite:///:memory:")

    class FakeSession(AsyncSession):
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

    # Patch _sessionmaker to return FakeSession instance
    def fake_sessionmaker():
        return FakeSession()

    monkeypatch.setattr(manager, "_sessionmaker", fake_sessionmaker)
    with pytest.raises(session_mod.InternalServiceError):
        async with manager.session():
            raise session_mod.SQLAlchemyError("Simulated session error")
