import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.config.core import get_settings

logger.info("Starting application...")
settings = get_settings()
app = FastAPI()


if __name__ == "__main__":
    # just in developement to enable run uv run app\main.py
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=8000, reload=True)
