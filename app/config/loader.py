import os
from functools import lru_cache
from pathlib import Path

from loguru import logger

from app.config.cfg_core import DEFAULT_ENV_FILE, Settings


@lru_cache
def get_settings(_env_file: str | Path | None = None) -> Settings:
    """Prioritas:.

    1. Argumen _env_filer

    2. ENV_FILE dari environment variable
    3. DEFAULT_ENV_FILE (.env)
    """
    env_file = _env_file or os.getenv("ENV_FILE", DEFAULT_ENV_FILE)
    logger.info(f"Loading settings from {env_file}")
    return Settings(_env_file=env_file, _env_file_encoding="utf-8")  # type: ignore
