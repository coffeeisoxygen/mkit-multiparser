import inspect
import logging
from pathlib import Path

from loguru import logger
from loguru_config import LoguruConfig

from app.config.core import get_settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def hide_sensitive_data(record):
    # Mask credit card numbers
    import re

    record["message"] = re.sub(
        r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        "XXXX-XXXX-XXXX-XXXX",
        record["message"],
    )
    # Mask email addresses
    record["message"] = re.sub(
        r"\b[\w.-]+@[\w.-]+\.\w+\b", "***@***.***", record["message"]
    )


logyamlpath = Path(__file__).parent.parent.parent / "logconfig.yaml"
logconfig = LoguruConfig.load(logyamlpath)
# sampai sini maka obj logger sudah ada setup nya , kita overide dsini
overenv = get_settings().APP_ENV.value
logger.configure(extra={"env": overenv}, patcher=hide_sensitive_data)
