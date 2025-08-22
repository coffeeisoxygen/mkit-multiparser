"""setup cross origin."""

# Path To Setup
from typing import Any

from fastapi.middleware.cors import CORSMiddleware

from app.config import cfg_cors

a_origins = cfg_cors.ConfigCors().allow_origins
a_credentials = cfg_cors.ConfigCors().allow_credentials
a_methods = cfg_cors.ConfigCors().allow_methods
a_headers = cfg_cors.ConfigCors().allow_headers


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
