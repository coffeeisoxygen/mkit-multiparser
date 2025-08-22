from fastapi.responses import JSONResponse

from app.exception import AppExceptionError


def setup_exception(app) -> None:
    """Register custom exception handlers to FastAPI app.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.exception_handler(AppExceptionError)
    def app_exception_handler(_, exc: AppExceptionError):
        return JSONResponse(
            status_code=exc.status_code or 500,
            content=exc.to_dict(),
        )
