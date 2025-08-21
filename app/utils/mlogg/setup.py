import inspect
import logging
from pathlib import Path

import yaml
from app.utils.mlogg.utils import exception_patcher, masking_patcher, traceback_patcher
from loguru import logger
from loguru_config import LoguruConfig

logconfigpath = Path(__file__).parent.parent.parent.parent / "logconfig.yaml"


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


def patcher_wrapper(
    record: logging.LogRecord,
    masking_config: dict | None = None,
    exception_config: dict | None = None,
    traceback_config: dict | None = None,
) -> None:
    """Wrapper agar semua patcher config bisa diakses oleh patcher."""
    if masking_config is not None:
        masking_patcher(record, masking_config)
    if exception_config is not None:
        exception_patcher(record, exception_config)
    if traceback_config is not None:
        traceback_patcher(record, traceback_config)


def configure_logging(config_path: str | Path) -> None:
    """Setup logging: intercept stdlib, propagate loggers, masking, exception, traceback, and loguru config.

    Args:
        config_path: Path to YAML config file.
    """
    with open(config_path, encoding="utf-8") as file:
        config_dict = yaml.safe_load(file)

    dict_maskingsetup = config_dict.pop("masking", {})
    dict_propogate_setup = config_dict.pop("propogate", {})
    dict_exception_setup = config_dict.pop("exception_format", {})
    dict_traceback_setup = config_dict.pop("traceback_format", {})
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    if dict_propogate_setup.get("enabled", False):
        for logger_name in dict_propogate_setup.get("loggers_name", []):
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = []
            logging_logger.propagate = True
            if "level_to_pass" in dict_propogate_setup:
                logging_logger.setLevel(dict_propogate_setup["level_to_pass"])

    LoguruConfig.load(config_or_file=config_dict)
    LoguruConfig(
        extra={"env": "test masking"},
        patcher=lambda record: patcher_wrapper(
            record=record,  # pyright: ignore[reportArgumentType]
            masking_config=dict_maskingsetup,
            exception_config=dict_exception_setup,
            # traceback_config=dict_traceback_setup,
        ),  # type: ignore
    ).configure()
