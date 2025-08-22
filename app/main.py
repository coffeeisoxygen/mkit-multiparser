# ruff : noqa
from pathlib import Path

import uvicorn
from app._version import __version__ as version
from app.config import get_settings
from app.custom import (
    IPFilter,
    LoggingMiddleware,
    ip_protected,
    setup_cors,
    setup_lifespan,
)
from app.exception import AppExceptionError
from app.utils.mlogg import configure_logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

# Override If Needed with passing .env file
settings = get_settings()
# logging need env values , optional can be moved if needed
logconfigpath = Path(__file__).parent.parent / "config_log.yaml"
configure_logging(logconfigpath, settings.APP_ENV.value)
# Filtering IP
BLOCKED_IPS_DATA_ENDPOINT = ["127.0.0.1"]
ip_filter_data_endpoint = IPFilter(blocked_ips=set(BLOCKED_IPS_DATA_ENDPOINT))
# Main FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    version=version,
    debug=settings.APP_DEBUG,
    description="aplikasi untuk helper parsing reply addon json yang panjang panjang",
    lifespan=setup_lifespan,
)
# CORS
setup_cors(app)
# middlewares
app.add_middleware(LoggingMiddleware)


# adding custom exceptions
@app.exception_handler(AppExceptionError)
async def app_exception_handler(request: Request, exc: AppExceptionError):  # noqa: ARG001, D103, RUF029
    return JSONResponse(
        status_code=exc.status_code or 500,
        content=exc.to_dict(),
    )


@app.get("/")
async def root():  # noqa: D103
    return {"message": "Hello World"}


# demo ip filtering mode direct IP Assignment
@app.get("/debug")
@ip_protected(IPFilter(allowed_ips={"10.0.0.1"}))
async def debug_endpoint(request: Request):  # noqa: D103
    return {"message": "This is a debug endpoint"}


# demo Ip filtering Based On Blocked List
@app.get("/blocked")
@ip_protected(ip_filter_data_endpoint)
async def blocked_endpoint(request: Request):  # noqa: D103
    return {"message": "This is a blocked endpoint"}


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
