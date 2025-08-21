# Import logging setup first!
import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.config import get_settings
from app.config.lifespan import app_lifespan

logger.info("Starting application...")
logger.info("User paid with card 4532-1234-5678-9012")
logger.info("Contact email: john.doe@example.com")
# sampling jika ada di field extra
logger.bind(
    extra={
        "user_id": "12345",
        "transaction_id": "abcde-12345-fghij-67890",
        "payment_method": "credit_card",
        "token": "ini harus redacted",
    }
).info("Payment processed successfully.")
# sampling jika ada di log biasa
password = "password ini harus redacted"
logger.info(f"User password: {password}")

settings = get_settings()
app = FastAPI(lifespan=app_lifespan)


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
