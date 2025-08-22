"""setup cross origin."""

# Path To Setup
from typing import Any

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import cfg_cors
from app.exception.base import AppExceptionError
from app.router import rtr_admin

a_origins = cfg_cors.ConfigCors().allow_origins
a_credentials = cfg_cors.ConfigCors().allow_credentials
a_methods = cfg_cors.ConfigCors().allow_methods
a_headers = cfg_cors.ConfigCors().allow_headers


def setup_router(app):
    app.include_router(rtr_admin.router, prefix="/admin", tags=["admin"])


def setup_cors(app: Any) -> None:
    """Setup CORS middleware for the FastAPI application.

    This function configures the CORS middleware to allow requests from specified origins.

    Args:
        app (Any): The FastAPI application instance.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=a_origins,
        allow_credentials=a_credentials,
        allow_methods=a_methods,
        allow_headers=a_headers,
    )


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
