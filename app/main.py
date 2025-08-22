# ruff : noqa

from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.config import get_settings
from app.custom import LoggingMiddleware
from app.exception import setup_exception
from app.lifespan import setup_lifespan
from app.router import setup_router
from app.custom.mlogging.setup import setup_logging

# NiceGUI integration
from nicegui import ui
# Import trimmer page to register it

# Setup settings and logging
settings = get_settings()
logconfigpath = Path(__file__).parent.parent / "config_log.yaml"
setup_logging(config_path=logconfigpath, env=settings.APP.environment.value)
# setup_logging()
logger.bind(sample="value").info("field extra harus bersih")
# Main FastAPI Application
app = FastAPI(
    title=settings.APP.name,
    version=settings.APP.version,
    debug=settings.APP.debug,
    description="aplikasi untuk helper parsing reply addon json yang panjang panjang",
    lifespan=setup_lifespan,
)
# middlewares
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=settings.CORS.allow_origins,
    allow_credentials=settings.CORS.allow_credentials,
    allow_methods=settings.CORS.allow_methods,
    allow_headers=settings.CORS.allow_headers,
)

app.add_middleware(middleware_class=LoggingMiddleware)


# routers
setup_router(app)
# exceptions
setup_exception(app)


@app.get("/")
async def root():  # noqa: D103
    return {"message": "Hello World"}


if __name__ == "__main__":
    # Mount NiceGUI to FastAPI app at /ui
    ui.run_with(app, mount_path="/ui")
    logger.info("Running application with Uvicorn...")
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
        log_level=None,
    )
