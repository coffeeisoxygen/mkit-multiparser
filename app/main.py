# ruff : noqa

from pathlib import Path
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.config import get_settings
from app.custom import LoggingMiddleware, setup_logging
from app.exception import setup_exception
from app.lifespan import setup_lifespan
from app.router import setup_router


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

# Mount static files and templates for UI
app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")
templates = Jinja2Templates(directory="app/ui/templates")

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


# Endpoint render index.html (UI)
@app.get("/ui")
async def ui_index(request: Request):
    """Render UI index page."""
    return templates.TemplateResponse("index.html", {"request": request})


# Default root endpoint
@app.get("/")
async def root():  # noqa: D103
    return {"message": "Hello World"}


if __name__ == "__main__":
    # Mount NiceGUI to FastAPI app at /ui

    logger.info("Running application with Uvicorn...")
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
        log_level=None,
    )
