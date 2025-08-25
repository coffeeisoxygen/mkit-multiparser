from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from app.exception import PasswordInternalError
from app.utils.hasher import HasherInterface


class Argon2Hasher(HasherInterface):
    """Implementasi hasher dengan argon2-cffi."""

    def __init__(self):
        self._hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        """Verify a password against a given hash.

        Args:
            password (str): The password to verify.
            hashed (str): The hash to verify against.

        Returns:
            bool: True if verification succeeds.

        Raises:
            PasswordInternalError: If verification fails or hash is invalid.
        """
        try:
            return self._hasher.verify(hashed, password)
        except (InvalidHashError, VerificationError, VerifyMismatchError) as exc:
            raise PasswordInternalError(f"Password verification failed: {exc}") from exc
