"""test configuration."""

import logging
from pathlib import Path

import pytest
from app.config import get_settings
from app.custom.mlogging.setup import InterceptHandler
from app.exception.loader import setup_exception
from fastapi import FastAPI
from loguru import logger

DIGIPOS_VALID_NUMBER = "081295221539"
DIGIPOS_INVALID_NUMBER = "081296221639"
DIGIPOS_PAYMENT_METHOD = "LINKAJA"


@pytest.fixture(scope="function", autouse=True)
def test_settings():
    """
    Test settings fixture for the testing environment.

    This fixture provides the application settings for the testing environment.

    Returns:
        _type_: The application settings for the testing environment.
    """
    get_settings.cache_clear()
    test_env = Path(__file__).parent.parent / ".env.test"
    settings = get_settings(test_env)
    # print(f"values {settings}")
    return settings


@pytest.fixture(autouse=True)
def intercept_loguru(caplog: pytest.LogCaptureFixture):
    # Intercept standard logging to loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    handler_id = logger.add(
        sink=caplog.handler,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        enqueue=False,
    )
    yield
    logger.remove(handler_id)


@pytest.fixture
def app_with_exception():
    app = FastAPI()
    setup_exception(app)
    return app
