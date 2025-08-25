from typing import Protocol

from app.schemas.token import TokenPayload


class ITokenService(Protocol):
    """Protocol for TokenService.

    Token akan menggunakan username sebagai sub (subject claim).
    """

    expire_minutes: int

    def create_token(self, username: str, is_superuser: bool, is_active: bool) -> str:
        """Create JWT token dengan sub = username."""
        ...

    def decode_token(self, token: str) -> TokenPayload:
        """Decode JWT token dan validate ke TokenPayload schema."""
        ...
