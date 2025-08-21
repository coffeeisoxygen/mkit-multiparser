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
