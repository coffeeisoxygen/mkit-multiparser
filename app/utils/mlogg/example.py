"""Example usage of mlogg patchers and decorator.

Demonstrates both normal logging and exception logging using loguru.
"""

from pathlib import Path

from app.utils.mlogg.setup import configure_logging
from loguru import logger

logconfigpath = Path(__file__).parent.parent.parent.parent / "logconfig.yaml"
configure_logging(logconfigpath)


def normal_case():
    """Logs a normal info message."""
    logger.info("Normal case executed successfully.")


def exception_case(x: int):
    """Logs an exception if division by zero occurs.

    Args:
        x (int): Denominator for division.
    """
    try:
        result = 10 / x
        logger.info(f"Division result: {result}")
    except ZeroDivisionError:
        logger.exception("Exception case: Division by zero occurred.")


if __name__ == "__main__":
    normal_case()
    exception_case(0)
