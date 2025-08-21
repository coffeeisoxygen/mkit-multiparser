import inspect
import logging
from pathlib import Path

import yaml
from app.utils.mlogg.utils import masking_patcher
from loguru import logger
from loguru_config import LoguruConfig

logconfigpath = Path(__file__).parent.parent.parent.parent / "logconfig.yaml"

with open(logconfigpath, encoding="utf-8") as file:
    config_dict = yaml.safe_load(file)

dict_maskingsetup = config_dict.pop("masking", {})


def patcher_wrapper(record):
    """Wrapper agar masking config bisa diakses oleh patcher."""
    masking_patcher(record, dict_maskingsetup)


class InterceptHandler(logging.Handler):
    """Handler to intercept standard logging and forward to loguru.

    Use this to unify stdlib logging and loguru output.
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_logging() -> None:
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    LoguruConfig.load(config_or_file=config_dict)
    LoguruConfig(extra={"env": "test masking"}, patcher=patcher_wrapper).configure()
