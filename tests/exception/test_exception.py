import pytest
from app.exception.base import AppExceptionError
from app.exception.exceptions import IPBlockedError, RequestValidationError

pytestmark = pytest.mark.unit


def test_app_exception_error_basic():
    # Arrange
    msg = "Custom error message"
    ctx = {"foo": "bar"}
    # Act
    exc = AppExceptionError(message=msg, context=ctx)
    # Assert
    assert exc.message == msg
    assert exc.context == ctx
    assert exc.status_code is None
    assert isinstance(str(exc), str)
    assert isinstance(repr(exc), str)


def test_app_exception_error_chaining():
    # Arrange
    cause = ValueError("invalid value")
    # Act
    exc = AppExceptionError(message="Has cause", cause=cause)
    # Assert
    assert "caused by ValueError" in str(exc)
    assert exc.__cause__ == cause


def test_app_exception_error_to_dict():
    # Arrange
    exc = AppExceptionError(message="Dict test", context={"x": 1})
    # Act
    result = exc.to_dict()
    # Assert
    assert result["name"] == exc.name
    assert result["message"] == exc.message
    assert result["context"] == {"x": 1}
    assert result["status_code"] is None


def test_request_validation_error_default():
    # Act
    exc = RequestValidationError()
    # Assert
    assert exc.message == exc.default_message
    assert exc.status_code == 422


def test_ip_blocked_error_context():
    # Arrange
    ip = "1.2.3.4"
    endpoint = "/api/test"
    # Act
    exc = IPBlockedError(ip=ip, endpoint=endpoint)
    # Assert
    assert exc.context["ip"] == ip
    assert exc.context["endpoint"] == endpoint
    assert exc.status_code == 403
