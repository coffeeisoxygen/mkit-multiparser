from typing import Protocol


class HasherInterface(Protocol):
    """Protocol untuk password hasher."""

    def hash(self, password: str) -> str:
        """Hash password dan return hasilnya."""
        ...

    def verify(self, password: str, hashed: str) -> bool:
        """Verifikasi password dengan hash."""
        ...
