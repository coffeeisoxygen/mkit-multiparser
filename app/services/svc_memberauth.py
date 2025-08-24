"""services untuk auth member."""

from app.schemas import MemberTrxRequest
from app.services.siganture.interface import ISignatureService


class MemberAuthService:
    """Service untuk autentikasi member."""

    def __init__(self, signature_service: ISignatureService):
        self.signature_service = signature_service

    def authenticate(self, request: MemberTrxRequest) -> bool:
        """Autentikasi member berdasarkan request.

        Raises:
            ValueError: Jika sign, pin, atau password bernilai None.
        """
        if request.sign is None:
            raise ValueError("Signature (sign) tidak boleh None")
        if request.pin is None:
            raise ValueError("PIN tidak boleh None")
        if request.password is None:
            raise ValueError("Password tidak boleh None")
        return self.signature_service.verify_signature(
            request.sign,
            request.memberid,
            request.product,
            request.dest,
            request.refid,
            request.pin,
            request.password,
        )
