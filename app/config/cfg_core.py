"""project environments configurations."""

# ruff:noqa
#
from enum import StrEnum
from typing import TYPE_CHECKING

from app.config.cfg_cors import ConfigCors

from app.config.cfg_env import ConfigEnvironment
from app.config.cfg_jwt import ConfigJwt


if TYPE_CHECKING:
    from app._version import __version__ as version

from pathlib import Path

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
        env_nested_delimiter="__",
        extra="ignore",
        case_sensitive=False,
    )

    APP: ConfigEnvironment = ConfigEnvironment()
    CORS: ConfigCors = ConfigCors()
    JWT: ConfigJwt = ConfigJwt()
