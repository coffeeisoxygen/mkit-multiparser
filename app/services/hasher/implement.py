from app.services.hasher.interface import HasherInterface
from argon2 import PasswordHasher
from argon2 import exceptions as argon2_exceptions


class Argon2Hasher(HasherInterface):
    """Implementasi hasher dengan argon2-cffi."""

    def __init__(self):
        self._hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        try:
            return self._hasher.verify(hashed, password)
        except argon2_exceptions.VerifyMismatchError:
            return False
