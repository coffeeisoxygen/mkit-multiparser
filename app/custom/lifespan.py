"""configure lifespan here."""

from contextlib import asynccontextmanager


@asynccontextmanager
async def setup_lifespan(app):  # noqa: ANN001, ARG001, RUF029
    """Lifespan context manager for the FastAPI application."""
    # do something here
    yield
    # clean here
