import inspect
import logging
from pathlib import Path

from loguru import logger
from loguru_config import LoguruConfig

from app.config.logpatch import redact_password


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


# NOTE: make sure harus terakhir di panggil karena ini akan mereset default, config, jadi jika mau custom, harus di atas
logyamlpath = Path(__file__).parent.parent.parent / "logging.yaml"

config = LoguruConfig.load(logyamlpath)
if config is not None:
    config.parse().configure()  # type: ignore
    logger = logger.patch(redact_password)
else:
    logger.warning(
        f"Loguru config not loaded from {logyamlpath}, using default logger configuration."
    )
