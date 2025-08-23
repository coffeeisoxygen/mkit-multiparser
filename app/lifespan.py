"""configure lifespan here."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.config import get_settings
from app.database.core.session import DatabaseSessionManager

# Your sessionmanager from above
sessionmanager = DatabaseSessionManager(get_settings().DB.url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application starting up.")
    # Nothing to do here if you initialize the manager at module level
    yield
    # Shutdown
    logger.info("Application shutting down.")
    await sessionmanager.close()
