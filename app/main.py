# Import logging setup first!
from pathlib import Path

import uvicorn
from app._version import __version__ as version
from app.config import app_lifespan, get_settings, setup_cors
from app.utils.mlogg import configure_logging
from fastapi import FastAPI
from loguru import logger

# Override If Needed with passing .env file
settings = get_settings()
# logging need env values , optional can be moved if needed
logconfigpath = Path(__file__).parent.parent / "logconfig.yaml"
configure_logging(logconfigpath, settings.APP_ENV.value)

# Main FastAPI Application
app = FastAPI(
    title="Addon MultiParser",
    version=version,
    description="aplikasi untuk helper parsing reply addon json yang panjang panjang",
    lifespan=app_lifespan,
)
# CORS
setup_cors(app)

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
