"""test configuration."""

import logging
from pathlib import Path

import pytest
from app.config import get_settings
from app.config.cfg_env import EnvironmentEnums
from app.custom.mlogging.setup import InterceptHandler
from loguru import logger


@pytest.fixture(scope="function", autouse=True)
def test_settings():
    """
    Test settings fixture for the testing environment.

    This fixture provides the application settings for the testing environment.

    Returns:
        _type_: The application settings for the testing environment.
    """
    get_settings.cache_clear()
    env_path = Path(__file__).parent.parent / ".env.test"
    settings = get_settings(_env_file=env_path)
    print(f"Using environment file: {env_path}")
    settings.APP.environment = EnvironmentEnums.TESTING
    # overriding manually
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
