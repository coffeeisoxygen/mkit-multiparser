"""test configuration."""

import pytest
from app.env_settings import get_settings


@pytest.fixture(scope="session")
def test_settings():
    """
    Test settings fixture for the testing environment.

    This fixture provides the application settings for the testing environment.

    Returns:
        _type_: The application settings for the testing environment.
    """
    return get_settings(_env_file=".env.test")
