"""configure lifespan here."""

from contextlib import asynccontextmanager

from app.utils.mlogg.setup import configure_logging


@asynccontextmanager
async def app_lifespan(app):  # noqa: ANN001, ARG001, RUF029
    """Lifespan context manager for the FastAPI application."""
    # do something here
    configure_logging()
    yield
    # clean here
