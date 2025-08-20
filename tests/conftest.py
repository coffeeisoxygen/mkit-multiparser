"""test configuration."""

import pytest
from app.config import get_settings
from loguru import logger


@pytest.fixture(scope="session")
def test_settings():
    """
    Test settings fixture for the testing environment.

    This fixture provides the application settings for the testing environment.

    Returns:
        _type_: The application settings for the testing environment.
    """
    return get_settings(_env_file=".env.test")


@pytest.fixture(autouse=True)
def intercept_loguru(caplog: pytest.LogCaptureFixture):
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
