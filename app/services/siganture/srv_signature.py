"""OtomaxSignatureService: Concrete implementation for OtomaX signature generation and verification."""

import base64
import hashlib


class OtomaxSignatureService:
    """Service untuk generate dan verifikasi signature OtomaX API."""

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
        raw = f"OtomaX|{memberid.upper()}|{product.upper()}|{dest}|{refid}|{pin}|{password}"
        sha1_digest = hashlib.sha1(raw.encode()).digest()
        signature = base64.b64encode(sha1_digest).decode().rstrip("=")
        signature = signature.replace("+", "-").replace("/", "_")
        return signature

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
        expected = self.generate_signature(
            memberid, product, dest, refid, pin, password
        )
        return signature == expected
