from pydantic import field_validator
from pydantic_settings import BaseSettings

from app.config.cfg_core import StrEnum


class EnvironmentEnums(StrEnum):
    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"


class ConfigEnvironment(BaseSettings):
    environment: EnvironmentEnums = EnvironmentEnums.PRODUCTION
    name: str = "MKIT_WRAPPER"
    version: str = "0.1.0"
    debug: bool = False

    @field_validator("environment", mode="before")
    @classmethod
    def normalize_env(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.upper()
        return v
