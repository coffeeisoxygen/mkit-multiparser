"""Example usage of mlogg patchers and decorator."""

from pathlib import Path

from app.utils.mlogg.setup import configure_logging
from loguru import logger

logconfigpath = Path(__file__).parent.parent.parent.parent / "logconfig.yaml"
configure_logging(logconfigpath)


# sample traceback happened
def main(x):
    # sample exception happened
    try:
        1 / x
    except ZeroDivisionError:
        logger.exception("Oups...")
        return  # <-- ini penting!


if __name__ == "__main__":
    main(0)
