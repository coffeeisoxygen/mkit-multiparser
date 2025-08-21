# Import logging setup first!
from fastapi import FastAPI
from loguru import logger

from app.config.core import get_settings

logger.info("Starting application...")
logger.info("User paid with card 4532-1234-5678-9012")
logger.info("Contact email: john.doe@example.com")
settings = get_settings()
app = FastAPI()
