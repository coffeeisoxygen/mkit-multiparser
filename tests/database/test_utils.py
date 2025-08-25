import pytest
from app.database.core import db_performance_metrics
from app.database.core.session import sessionmanager

# app/database/core/test_utils.py


@pytest.mark.asyncio
async def test_db_performance_metrics_success(db_session):
    """
    Test db_performance_metrics returns ok status and ping_time_ms on success.
    """
    result = await db_performance_metrics()
    assert result["status"] == "ok"
    assert isinstance(result["ping_time_ms"], float)
    assert result["ping_time_ms"] > 0


@pytest.mark.asyncio
async def test_db_performance_metrics_engine_none(monkeypatch):
    """
    Test db_performance_metrics returns error if engine is None.
    """
    monkeypatch.setattr(sessionmanager, "engine", None)
    result = await db_performance_metrics(engine=None)
    assert result["status"] == "error"
    assert result["ping_time_ms"] is None
    assert "Engine is not initialized" in result["details"]


@pytest.mark.asyncio
async def test_db_performance_metrics_connection_error(monkeypatch):
    """
    Test db_performance_metrics returns error if connection fails.
    """

    class FakeConnection:
        async def __aenter__(self):
            raise Exception("Connection failed")

        async def __aexit__(self, exc_type, exc, tb):
            pass

    class FakeEngine:
        def connect(self):
            return FakeConnection()

    result = await db_performance_metrics(engine=FakeEngine())
    assert result["status"] == "error"
    assert isinstance(result["ping_time_ms"], float)
    assert "Connection failed" in result["details"]


@pytest.mark.asyncio
async def test_db_performance_metrics_ping_time_is_reasonable():
    """
    Test ping_time_ms is within reasonable bounds.
    """
    result = await db_performance_metrics()
    assert result["status"] == "ok"
    # Should be less than 500ms for local sqlite
    assert 0 < result["ping_time_ms"] < 500
