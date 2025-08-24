from abc import ABC, abstractmethod


class HasherInterface(ABC):
    """Interface untuk password hasher."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash password dan return hasilnya."""
        pass

    @abstractmethod
    def verify(self, password: str, hashed: str) -> bool:
        """Verifikasi password dengan hash."""
        pass
