from loguru import logger


def test_test_settings_fixture(test_settings):
    """Ensure test_settings fixture returns correct values for testing."""
    # Adjusted to match nested config structure
    assert test_settings.APP.environment.value == "TESTING"
    assert isinstance(test_settings.APP.debug, bool)
    assert "sqlite" in test_settings.DB_URL
    assert isinstance(test_settings.APP.name, str)


def test_loguru_intercept(caplog):
    """Ensure loguru logs are intercepted and can be asserted via caplog."""
    logger.info("Hello from loguru!")
    assert "Hello from loguru!" in caplog.text
