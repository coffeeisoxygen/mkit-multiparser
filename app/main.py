# ruff : noqa
from pathlib import Path

import uvicorn
from app._version import __version__ as version
from app.config import get_settings
from app.custom import (
    LoggingMiddleware,
    setup_cors,
    setup_lifespan,
)
from app.exception.base import setup_exception
from app.router import setup_router
from app.utils.mlogg import configure_logging
from fastapi import FastAPI
from loguru import logger

# Override If Needed with passing .env file
settings = get_settings()
# logging need env values , optional can be moved if needed
logconfigpath = Path(__file__).parent.parent / "config_log.yaml"
configure_logging(logconfigpath, settings.APP.environment.value)


# Main FastAPI Application
app = FastAPI(
    title=settings.APP.name,
    version=version,
    debug=settings.APP.debug,
    description="aplikasi untuk helper parsing reply addon json yang panjang panjang",
    lifespan=setup_lifespan,
)

# middlewares
app.add_middleware(LoggingMiddleware)
# CORS
setup_cors(app)
# routers
setup_router(app)
# exceptions
setup_exception(app)


@app.get("/")
async def root():  # noqa: D103
    return {"message": "Hello World"}


if __name__ == "__main__":
    logger.info("Running application with Uvicorn...")
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
        log_level=None,
    )
