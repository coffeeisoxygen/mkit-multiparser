"""configurasi JWT dan kawan kawan."""

from pydantic_settings import BaseSettings


class ConfigJwt(BaseSettings):
    """Konfigurasi JWT."""

    SECRET_KEY: str = "test key jwt"
    ALGORITHM: str = "test algorithm"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


class ConfigSession(BaseSettings):
    """Konfigurasi Session.

    MAX_ACTIVE_SESSIONS_PER_USER: jumlah maksimal session aktif per user.
    DEFAULT_SESSION_EXPIRE_MINUTES: waktu default session expired (menit).
    SESSION_CONCURRENCY_POLICY: "single" (hanya 1 session aktif) atau "multi" (boleh lebih dari 1).
    SESSION_LOGGING_ENABLED: aktifkan logging session.
    """

    MAX_ACTIVE_SESSIONS_PER_USER: int = 3
    DEFAULT_SESSION_EXPIRE_MINUTES: int = 60
    SESSION_CONCURRENCY_POLICY: str = "multi"  # "single" or "multi"
    SESSION_LOGGING_ENABLED: bool = True
