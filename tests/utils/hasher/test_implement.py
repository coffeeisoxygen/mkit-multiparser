import pytest
from app.utils.hasher.implement import Argon2Hasher


@pytest.fixture
def hasher():
    return Argon2Hasher()


def test_hash_and_verify_success(hasher):
    # Arrange
    password = "securepassword123"
    # Act
    hashed = hasher.hash(password)
    # Assert
    assert isinstance(hashed, str)
    assert hasher.verify(password, hashed) is True


def test_verify_wrong_password(hasher):
    # Arrange
    password = "mypassword"
    wrong_password = "notmypassword"
    hashed = hasher.hash(password)
    # Act
    result = hasher.verify(wrong_password, hashed)
    # Assert
    assert result is False


def test_verify_invalid_hash(hasher):
    # Arrange
    password = "testpass"
    invalid_hash = "not_a_valid_hash"
    # Act
    result = hasher.verify(password, invalid_hash)
    # Assert
    assert result is False
