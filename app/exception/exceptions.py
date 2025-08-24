from typing import Any

from app.exception.base import AppExceptionError


class RequestValidationError(AppExceptionError):
    """Raised when request validation fails.

    This exception is used to indicate that the request data is invalid
    and does not conform to the expected schema.

    Args:
        AppExceptionError (_type_): _description_
    """

    default_message: str = "Request validation error occurred."
    status_code: int | None = 422


class IPBlockedError(AppExceptionError):
    """Exception kalau IP di-blacklist atau tidak allowed."""

    default_message: str = "Forbidden: IP address tidak diizinkan."
    status_code: int | None = 403

    def __init__(self, ip: str, endpoint: str, context: dict[str, Any] | None = None):
        ctx = context or {}
        ctx.update({"ip": ip, "endpoint": endpoint})

        super().__init__(
            message=self.default_message,
            context=ctx,
        )


# group related to internal services
class InternalServiceError(AppExceptionError):
    """Exception untuk kesalahan internal server."""

    default_message: str = "Internal server error occurred."
    status_code: int | None = 500


# Group User exceptions Error
class UserGenericError(AppExceptionError):
    """Exception untuk kesalahan umum pada user."""

    default_message: str = "User error occurred."
    status_code: int | None = 400


class UserNotFoundError(UserGenericError):
    """Exception untuk user tidak ditemukan."""

    default_message: str = "User not found."
    status_code: int | None = 404


class UserDuplicateError(UserGenericError):
    """Exception untuk user duplikat."""

    default_message: str = "User already exists."
    status_code: int | None = 409


class UserCreationError(UserGenericError):
    """Exception untuk kesalahan saat membuat user."""

    default_message: str = "User creation failed."
    status_code: int | None = 400
