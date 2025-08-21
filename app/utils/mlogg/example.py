"""Example usage of mlogg patchers and decorator."""

from pathlib import Path

from app.utils.mlogg.setup import configure_logging
from loguru import logger


def main():
    logconfigpath = Path(__file__).parent.parent.parent.parent / "logconfig.yaml"
    configure_logging(logconfigpath)

    logger.info("Starting example...")
    logger.info("User paid with card 4532-1234-5678-9012")

    # # Sample function using log_exec_time decorator (sync)
    # @log_exec_time(level="INFO")
    # def process_payment(amount: float, method: str) -> str:
    #     """Simulate payment processing."""
    #     time.sleep(0.2)
    #     return f"Processed {amount} via {method}"

    # Sample async function using log_exec_time decorator
    # @log_exec_time(level="INFO")
    # async def fetch_user_data(user_id: str) -> dict:
    #     """Simulate async user data fetch."""
    #     await asyncio.sleep(0.1)
    #     return {"user_id": user_id, "name": "John Doe"}

    logger.info("Contact email: john.doe@example.com")
    logger.bind(
        extra={
            "user_id": "12345",
            "transaction_id": "abcde-12345-fghij-67890",
            "payment_method": "credit_card",
            "token": "ini harus redacted",
        }
    ).info("Payment processed successfully.")

    password = "password ini harus redacted"
    logger.info(f"User password: {password}")

    # # # Example: log exception with stackprinter/diagnose

    def inverse(x):
        try:
            1 / x
        except ZeroDivisionError:
            logger.exception("Oups... exception formatting demo")

    inverse(0)

    # Example: log with traceback (no exception)
    # logger.bind(with_traceback=True).info("This log includes a traceback")

    # # Call sync sample
    # result = process_payment(100_000, "credit_card")
    # logger.info(f"Result: {result}")

    # # Call async sample

    # user_data = asyncio.run(fetch_user_data("12345"))
    # logger.info(f"Fetched user data: {user_data}")


if __name__ == "__main__":
    main()
