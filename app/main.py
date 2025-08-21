# Import logging setup first!
from pathlib import Path

import uvicorn
from app.config import get_settings
from app.config.lifespan import app_lifespan
from app.utils.mlogg.setup import configure_logging
from fastapi import FastAPI
from loguru import logger

logconfigpath = Path(__file__).parent.parent / "logconfig.yaml"
configure_logging(logconfigpath)

settings = get_settings()
app = FastAPI(lifespan=app_lifespan)


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
