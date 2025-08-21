# Import logging setup first!
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.config import get_settings
from app.config.lifespan import app_lifespan
from app.utils.mlogg.decorators import log_exec_time
from app.utils.mlogg.setup import configure_logging

logconfigpath = Path(__file__).parent.parent / "logconfig.yaml"
configure_logging(logconfigpath)

logger.info("Starting application...")
logger.info("User paid with card 4532-1234-5678-9012")


# Sample function using log_exec_time decorator (sync)
@log_exec_time(level="INFO")
def process_payment(amount: float, method: str) -> str:
    """Simulate payment processing."""
    import time

    time.sleep(0.2)
    return f"Processed {amount} via {method}"


# Sample async function using log_exec_time decorator
@log_exec_time(level="INFO")
async def fetch_user_data(user_id: str) -> dict:
    """Simulate async user data fetch."""
    import asyncio

    await asyncio.sleep(0.1)
    return {"user_id": user_id, "name": "John Doe"}


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
    # Call sync sample
    result = process_payment(100_000, "credit_card")
    logger.info(f"Result: {result}")

    # Call async sample
    import asyncio

    user_data = asyncio.run(fetch_user_data("12345"))
    logger.info(f"Fetched user data: {user_data}")

    logger.info("Running application with Uvicorn...")
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
        log_level=None,
    )
