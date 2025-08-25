import pytest
from app.exception import PasswordInternalError
from app.utils.hasher.argon_hasher import Argon2Hasher


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


def test_verify_wrong_password_raises(hasher):
    # Arrange
    password = "mypassword"
    wrong_password = "notmypassword"
    hashed = hasher.hash(password)
    # Act & Assert
    with pytest.raises(PasswordInternalError):
        hasher.verify(wrong_password, hashed)


def test_verify_invalid_hash_raises(hasher):
    # Arrange
    password = "testpass"
    invalid_hash = "not_a_valid_hash"
    # Act & Assert
    with pytest.raises(PasswordInternalError):
        hasher.verify(password, invalid_hash)
