"""test configuration."""

import pytest
from app.env_settings import get_settings


@pytest.fixture(scope="session")
def test_settings():
    return get_settings(_env_file=".env.test")
