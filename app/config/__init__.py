"""project environments configurations."""

# ruff:noqa
#
from enum import StrEnum
from typing import TYPE_CHECKING

from app.config.cfg_cors import ConfigCors
from app.config.cfg_jwt import ConfigJwt


if TYPE_CHECKING:
    from app._version import __version__ as version

import os
from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_ENV_FILE = BASE_DIR / ".env"


class EnvironmentEnums(StrEnum):
    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    APP_ENV: EnvironmentEnums = EnvironmentEnums.PRODUCTION
    APP_DEBUG: bool = False
    APP_NAME: str = "MKIT_WRAPPER"
    CORS: ConfigCors = ConfigCors()
    JWT: ConfigJwt = ConfigJwt()

    # ADM_ID: uuid.UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")

    # DB_URL: str = "sqlite+aiosqlite:///./mkit.db"

    @field_validator("APP_ENV", mode="before")
    @classmethod
    def normalize_env(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.upper()
        return v


@lru_cache
def get_settings(_env_file: str | Path | None = None) -> Settings:
    """Prioritas:.

    1. Argumen _env_file
    2. ENV_FILE dari environment variable
    3. DEFAULT_ENV_FILE (.env)
    """
    env_file = _env_file or os.getenv("ENV_FILE", DEFAULT_ENV_FILE)
    return Settings(_env_file=env_file, _env_file_encoding="utf-8")  # type: ignore
