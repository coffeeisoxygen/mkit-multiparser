# Import logging setup first!
import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.config.core import get_settings

logger.info("Starting application...")
logger.info("User paid with card 4532-1234-5678-9012")
logger.info("Contact email: john.doe@example.com")
settings = get_settings()
app = FastAPI()


if __name__ == "__main__":
    logger.info("Starting application...")
    logger.info("Running application with Uvicorn...")
    uvicorn.run(
        app="app:main",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
        log_level=None,
    )
