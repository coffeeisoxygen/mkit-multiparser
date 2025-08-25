from argon2 import PasswordHasher
from argon2 import exceptions as argon2_exceptions

from app.utils.hasher import HasherInterface


class Argon2Hasher(HasherInterface):
    """Implementasi hasher dengan argon2-cffi."""

    def __init__(self):
        self._hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        try:
            return self._hasher.verify(hashed, password)
        except (
            argon2_exceptions.VerifyMismatchError,
            argon2_exceptions.InvalidHashError,
            argon2_exceptions.VerificationError,
        ):
            return False
