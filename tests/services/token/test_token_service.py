import jwt


def test_token_missing_sub():
    service = make_service()
    payload = {
        # 'sub' missing
        "is_superuser": True,
        "is_active": True,
        "exp": datetime.now(UTC) + timedelta(minutes=1),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(TokenInvalidError):
        service.decode_token(token)


def test_token_wrong_algorithm():
    service = make_service()
    user_id = 123
    username = "testuser"
    payload = {
        "sub": str(user_id),
        "username": username,
        "is_superuser": True,
        "is_active": True,
        "exp": datetime.now(UTC) + timedelta(minutes=1),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS512")
    with pytest.raises(TokenInvalidError):
        service.decode_token(token)


def test_token_exp_far_future():
    service = make_service()
    user_id = 123
    username = "testuser"
    payload = {
        "sub": str(user_id),
        "username": username,
        "is_superuser": True,
        "is_active": True,
        "exp": datetime.now(UTC) + timedelta(days=3650),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    decoded = service.decode_token(token)
    assert decoded.exp > datetime.now(UTC)


def test_token_with_random_claim():
    service = make_service()
    user_id = 123
    username = "testuser"
    payload = {
        "sub": str(user_id),
        "username": username,
        "is_superuser": True,
        "is_active": True,
        "exp": datetime.now(UTC) + timedelta(minutes=1),
        "random_claim": "random_value",
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    decoded = service.decode_token(token)
    assert hasattr(decoded, "sub")


def test_token_invalid_signature():
    service = make_service()
    user_id = 123
    username = "testuser"
    payload = {
        "sub": str(user_id),
        "username": username,
        "is_superuser": True,
        "is_active": True,
        "exp": datetime.now(UTC) + timedelta(minutes=1),
    }
    # Encode with wrong secret
    token = jwt.encode(payload, "wrongsecret", algorithm=ALGORITHM)
    with pytest.raises(TokenInvalidError):
        service.decode_token(token)


from datetime import UTC, datetime, timedelta

import pytest
from app.exception import TokenExpiredError, TokenInvalidError
from app.schemas.user.sch_user_token import TokenPayload
from app.services.token.srv_token import TokenService

SECRET_KEY = "testsecret"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 1


def make_service(expire_minutes=EXPIRE_MINUTES):
    return TokenService(SECRET_KEY, ALGORITHM, expire_minutes)


def test_create_and_decode_token():
    # Arrange
    service = make_service()
    user_id = 123
    username = "testuser"
    is_superuser = True
    is_active = True

    # Act
    token = service.create_token(user_id, username, is_superuser, is_active)
    payload = service.decode_token(token)

    # Assert
    assert isinstance(token, str)
    assert isinstance(payload, TokenPayload)
    assert payload.sub == str(user_id)
    assert payload.is_superuser is True
    assert payload.is_active is True
    assert payload.exp > datetime.now(UTC)


def test_expired_token():
    # Arrange
    service = make_service(expire_minutes=-1)  # expired
    user_id = 123
    username = "testuser"
    is_superuser = False
    is_active = True
    token = service.create_token(user_id, username, is_superuser, is_active)

    # Act & Assert
    with pytest.raises(TokenExpiredError):
        service.decode_token(token)


def test_invalid_token():
    # Arrange
    service = make_service()
    invalid_token = "invalid.jwt.token"

    # Act & Assert
    with pytest.raises(TokenInvalidError):
        service.decode_token(invalid_token)
