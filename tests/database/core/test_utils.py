from unittest.mock import AsyncMock

import pytest
from app.database.core.utils import db_health_check, db_performance_metrics


@pytest.mark.asyncio
async def test_db_health_check_success():
    mock_engine = AsyncMock()
    mock_conn = AsyncMock()
    mock_engine.connect.return_value.__aenter__.return_value = mock_conn
    mock_conn.execute.return_value = None

    result = await db_health_check(mock_engine)
    assert result["status"] == "ok"
    assert "DB connection successful" in result["details"]


@pytest.mark.asyncio
async def test_db_health_check_engine_none():
    result = await db_health_check(engine=None)
    assert result["status"] == "error"
    assert "Engine is not initialized" in result["details"]


@pytest.mark.asyncio
async def test_db_health_check_error():
    mock_engine = AsyncMock()
    mock_engine.connect.side_effect = Exception("DB error")
    result = await db_health_check(mock_engine)
    assert result["status"] == "error"
    assert "DB error" in result["details"]


@pytest.mark.asyncio
async def test_db_performance_metrics_success():
    mock_engine = AsyncMock()
    mock_conn = AsyncMock()
    mock_engine.connect.return_value.__aenter__.return_value = mock_conn
    mock_conn.execute.return_value = None

    result = await db_performance_metrics(mock_engine)
    assert result["status"] == "ok"
    assert isinstance(result["ping_time_ms"], float)


@pytest.mark.asyncio
async def test_db_performance_metrics_engine_none():
    result = await db_performance_metrics(engine=None)
    assert result["status"] == "error"
    assert result["ping_time_ms"] is None
    assert "Engine is not initialized" in result["details"]


@pytest.mark.asyncio
async def test_db_performance_metrics_error():
    mock_engine = AsyncMock()
    mock_engine.connect.side_effect = Exception("Timeout")
    result = await db_performance_metrics(mock_engine)
    assert result["status"] == "error"
    assert isinstance(result["ping_time_ms"], float)
    assert "Timeout" in result["details"]
