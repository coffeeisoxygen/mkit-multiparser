# Import logging setup first!
import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.config.core import get_settings

logger.info("Starting application...")
settings = get_settings()
app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
        log_level=None,
    )
