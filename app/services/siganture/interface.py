"""ISignatureService: Interface for OtomaX signature service."""

from typing import Protocol


class ISignatureService(Protocol):
    """Interface untuk OtomaX signature service."""

    def generate_signature(
        self,
        memberid: str,
        product: str,
        dest: str,
        refid: str,
        pin: str,
        password: str,
    ) -> str:
        """Generate OtomaX transaction signature."""
        ...

    def verify_signature(
        self,
        signature: str,
        memberid: str,
        product: str,
        dest: str,
        refid: str,
        pin: str,
        password: str,
    ) -> bool:
        """Verifikasi signature OtomaX transaction."""
        ...
