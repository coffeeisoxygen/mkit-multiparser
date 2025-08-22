"""OtomaX signature service."""

import base64
import hashlib


class OtomaxSignatureService:
    """Service untuk generate dan verifikasi signature OtomaX API."""

    @staticmethod
    def generate_signature(
        memberid: str, product: str, dest: str, refid: str, pin: str, password: str
    ) -> str:
        """Generate OtomaX transaction signature.

        Args:
            memberid: Member ID (will be converted to UPPERCASE)
            product: Product code (will be converted to UPPERCASE)
            dest: Destination phone number (original case)
            refid: Reference/Transaction ID (original case, can be numeric or alphanumeric)
            pin: Member PIN (original case)
            password: Member password (original case)

        Returns:
            str: Base64 encoded signature with URL-safe characters

        Examples:
            >>> service = OtomaxSignatureService()
            >>> service.generate_signature(
            ...     "vps",
            ...     "CLPDATA",
            ...     "081295221639",
            ...     "3040881",
            ...     "777999",
            ...     "vps777999",
            ... )
            'MsP6Aticed6s1rlEhvj4NKceFVQ'

            >>> service.generate_signature(
            ...     "vps",
            ...     "CLPDATA",
            ...     "081295221639",
            ...     "3040881LIST",
            ...     "777999",
            ...     "vps777999",
            ... )
            'pEGjrgXE0kSHupl8uSjPbODg7R4'

        Algorithm:
            1. Build raw string: OtomaX|MEMBERID|PRODUCT|dest|refid|pin|password
               - memberid and product are converted to UPPERCASE
               - Other fields maintain original case
            2. Generate SHA1 hash of raw string
            3. Base64 encode the hash
            4. Remove padding '=' characters
            5. Replace '+' with '-' and '/' with '_' for URL safety
        """
        raw = f"OtomaX|{memberid.upper()}|{product.upper()}|{dest}|{refid}|{pin}|{password}"
        sha1_digest = hashlib.sha1(raw.encode()).digest()
        signature = base64.b64encode(sha1_digest).decode().rstrip("=")
        signature = signature.replace("+", "-").replace("/", "_")
        return signature

    @staticmethod
    def verify_signature(
        signature: str,
        memberid: str,
        product: str,
        dest: str,
        refid: str,
        pin: str,
        password: str,
    ) -> bool:
        """Verifikasi signature OtomaX transaction.

        Args:
            signature: Signature yang akan diverifikasi.
            memberid: Member ID (akan diubah ke UPPERCASE).
            product: Product code (akan diubah ke UPPERCASE).
            dest: Destination phone number (original case).
            refid: Reference/Transaction ID (original case, bisa numeric/alphanumeric).
            pin: Member PIN (original case).
            password: Member password (original case).

        Returns:
            bool: True jika signature valid, False jika tidak
        """
        expected = OtomaxSignatureService.generate_signature(
            memberid, product, dest, refid, pin, password
        )
        return signature == expected
