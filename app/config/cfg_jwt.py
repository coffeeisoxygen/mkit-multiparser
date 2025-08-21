"""configurasi JWT dan kawan kawan."""

from pydantic_settings import BaseSettings


class ConfigJwt(BaseSettings):
    """Konfigurasi JWT."""

    SECRET_KEY: str = "test key jwt"
    ALGORITHM: str = "test algorithm"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
