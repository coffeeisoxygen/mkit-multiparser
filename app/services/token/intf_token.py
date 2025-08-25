from typing import Protocol

from app.schemas.user import TokenPayload


class ITokenService(Protocol):
    """Protocol for TokenService.

    Token akan menggunakan username sebagai sub (subject claim).
    """

    expire_minutes: int

    def create_token(
        self, user_id: int, username: str, is_superuser: bool, is_active: bool
    ) -> str:
        """Create JWT token dengan sub = user_id."""
        ...

    def decode_token(self, token: str) -> TokenPayload:
        """Decode JWT token dan validate ke TokenPayload schema."""
        ...
