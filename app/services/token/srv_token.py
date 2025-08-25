from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from app.exception import (
    TokenExpiredError,
    TokenGenericError,
    TokenInvalidError,
)
from app.schemas.token import TokenPayload
from app.services.token.intf_token import ITokenService
from loguru import logger


class TokenService(ITokenService):
    """Create & validate JWT."""

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
        logger.bind(service="TokenService").debug("TokenService initialized")

    def create_token(self, user_id: UUID, is_superuser: bool, is_active: bool) -> str:
        """Create JWT token with minimal payload."""
        expire = datetime.now(UTC) + timedelta(minutes=self.expire_minutes)

        payload = {
            "sub": str(user_id),
            "is_superuser": is_superuser,
            "is_active": is_active,
            "exp": expire,
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        logger.bind(service="TokenService").debug("Token created", user_id=str(user_id))
        return token

    def decode_token(self, token: str) -> TokenPayload:
        """Decode JWT token dan validate ke schema TokenPayload."""
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenPayload.model_validate(decoded)

        except jwt.ExpiredSignatureError as e:
            logger.bind(service="TokenService").warning("Token expired", token=token)
            raise TokenExpiredError(cause=e) from e
        except jwt.InvalidTokenError as e:
            logger.bind(service="TokenService").warning("Invalid token", token=token)
            raise TokenInvalidError(cause=e) from e
        except Exception as e:
            logger.bind(service="TokenService").error(
                "Authentication error occurred", token=token
            )
            raise TokenGenericError("Authentication error occurred.", cause=e) from e
