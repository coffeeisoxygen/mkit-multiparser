from typing import Protocol
from uuid import UUID

from app.schemas.token import TokenPayload


class ITokenService(Protocol):
    """Protocol for TokenService."""

    expire_minutes: int

    def create_token(self, user_id: UUID, is_superuser: bool, is_active: bool) -> str:
        """Create JWT token with minimal payload."""
        ...

    def decode_token(self, token: str) -> TokenPayload:
        """Decode JWT token and validate to TokenPayload schema."""
        ...
