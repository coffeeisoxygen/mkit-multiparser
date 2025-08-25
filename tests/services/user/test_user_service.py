from unittest.mock import AsyncMock, MagicMock

import pytest
from app.exception import UserCreationError, UserDuplicateError
from app.schemas.user.sch_user import UserCreate, UserPublicResponse
from app.services.user.srv_user import UserService
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_register_user_success():
    # Arrange
    user_repo = AsyncMock()
    user_repo.get_user_with_username.return_value = None
    user_repo.get_user_with_email.return_value = None
    user_repo.create_user.return_value = UserPublicResponse.model_validate({
        "id": 1,  # changed from "user-id" to int
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "created_at": None,
        "updated_at": None,
        "deleted_at": None,
    })
    hasher = MagicMock()
    hasher.hash.return_value = "hashed_pw"
    session_service = MagicMock()
    token_service = MagicMock()
    service = UserService(user_repo, hasher)
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        password="pwtest@90",
    )

    # Act
    result = await service.register_user(user_data)

    # Assert
    assert isinstance(result, UserPublicResponse)
    user_repo.get_user_with_username.assert_called_once_with("testuser")
    user_repo.get_user_with_email.assert_called_once_with("test@example.com")
    hasher.hash.assert_called_once_with("pwtest@90")
    user_repo.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_duplicate_username():
    # Arrange
    user_repo = AsyncMock()
    user_repo.get_user_with_username.return_value = MagicMock(id=1)  # id as int
    hasher = MagicMock()
    session_service = MagicMock()
    token_service = MagicMock()
    service = UserService(user_repo, hasher)
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        password="pwtest@90",
    )

    # Act & Assert
    with pytest.raises(UserDuplicateError):
        await service.register_user(user_data)


@pytest.mark.asyncio
async def test_register_user_duplicate_email():
    # Arrange
    user_repo = AsyncMock()
    user_repo.get_user_with_username.return_value = None
    user_repo.get_user_with_email.return_value = MagicMock(id=1)  # id as int
    hasher = MagicMock()
    session_service = MagicMock()
    token_service = MagicMock()
    service = UserService(user_repo, hasher)
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        password="pwtest@90",
    )

    # Act & Assert
    with pytest.raises(UserDuplicateError):
        await service.register_user(user_data)


@pytest.mark.asyncio
async def test_register_user_creation_error():
    # Arrange
    user_repo = AsyncMock()
    user_repo.get_user_with_username.return_value = None
    user_repo.get_user_with_email.return_value = None
    user_repo.create_user.return_value = None
    hasher = MagicMock()
    hasher.hash.return_value = "hashed_pw"

    service = UserService(user_repo, hasher)
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        password="pwtest@90",
    )

    # Act & Assert
    with pytest.raises(UserCreationError):
        await service.register_user(user_data)


def test_register_user_empty_username():
    with pytest.raises(ValidationError):
        UserCreate(
            username="", email="test@example.com", full_name="Test User", password="pw"
        )


def test_register_user_empty_email():
    with pytest.raises(ValidationError):
        UserCreate(username="testuser", email="", full_name="Test User", password="pw")


def test_register_user_empty_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            password="",
        )


def test_register_user_invalid_email_format():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="not-an-email",
            full_name="Test User",
            password="pwtest@90",
        )


def test_register_user_whitespace_username():
    with pytest.raises(ValidationError):
        UserCreate(
            username="   ",
            email="test@example.com",
            full_name="Test User",
            password="pwtest@90",
        )


def test_register_user_whitespace_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser", email="   ", full_name="Test User", password="pw"
        )


def test_register_user_special_char_username():
    with pytest.raises(ValidationError):
        UserCreate(
            username="!@#$%^&*()",
            email="test@example.com",
            full_name="Test User",
            password="pw",
        )


@pytest.mark.asyncio
async def test_register_user_case_sensitive_username():
    user_repo = AsyncMock()
    user_repo.get_user_with_username.side_effect = [
        None,
        {
            "id": 2,  # changed from "user-id" to int
            "username": "testuser",
            "email": "test2@example.com",
            "full_name": "Test User",
            "created_at": None,
            "updated_at": None,
            "deleted_at": None,
        },
    ]
    user_repo.get_user_with_email.return_value = None
    user_repo.create_user.return_value = {
        "id": 1,  # changed from "user-id" to int
        "username": "TestUser",
        "email": "test@example.com",
        "full_name": "Test User",
        "created_at": None,
        "updated_at": None,
        "deleted_at": None,
    }
    hasher = MagicMock()
    session_service = MagicMock()
    token_service = MagicMock()
    service = UserService(user_repo, hasher)
    user_data1 = UserCreate(
        username="TestUser",
        email="test@example.com",
        full_name="Test User",
        password="pwtest@90",
    )
    user_data2 = UserCreate(
        username="testuser",
        email="test2@example.com",
        full_name="Test User",
        password="pwtest@90",
    )
    await service.register_user(user_data1)
    with pytest.raises(UserDuplicateError):
        await service.register_user(user_data2)


def test_register_user_empty_full_name():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser", email="test@example.com", full_name="", password="pw"
        )


def test_register_user_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            password="pw",
        )
