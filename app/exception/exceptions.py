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
