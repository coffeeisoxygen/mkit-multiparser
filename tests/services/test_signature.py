import pytest
from app.services.siganture.srv_signature import OtomaxSignatureService

pytestmark = pytest.mark.unit


def test_signature_otomax_refid_sample():
    """Pastikan signature sesuai sample OtomaX untuk refID=3042220LIST."""
    service = OtomaxSignatureService()
    sig = service.generate_signature(
        "AKSES01", "CLPDATA", "081295221639", "3042220LIST", "777999", "vps777999"
    )
    assert sig == "XmgNy8YxklljuM8lBsrMVnhX7uc"


def test_generate_signature_with_list_refid():
    service = OtomaxSignatureService()
    sig = service.generate_signature(
        "vps", "CLPDATA", "081295221639", "3040881LIST", "777999", "vps777999"
    )
    assert sig == "pEGjrgXE0kSHupl8uSjPbODg7R4"


def test_verify_signature_valid():
    service = OtomaxSignatureService()
    sig = service.generate_signature(
        "vps", "CLPDATA", "081295221639", "3040881", "777999", "vps777999"
    )
    assert (
        service.verify_signature(
            sig, "vps", "CLPDATA", "081295221639", "3040881", "777999", "vps777999"
        )
        is True
    )


def test_verify_signature_invalid():
    service = OtomaxSignatureService()
    sig = service.generate_signature(
        "vps", "CLPDATA", "081295221639", "3040881", "777999", "vps777999"
    )
    # Ubah satu karakter
    assert (
        service.verify_signature(
            sig[:-1] + "X",
            "vps",
            "CLPDATA",
            "081295221639",
            "3040881",
            "777999",
            "vps777999",
        )
        is False
    )


@pytest.mark.parametrize(
    "memberid,product,dest,refid,pin,password",
    [
        ("", "CLPDATA", "081295221639", "3040881", "777999", "vps777999"),
        ("vps", "", "081295221639", "3040881", "777999", "vps777999"),
        ("vps", "CLPDATA", "", "3040881", "777999", "vps777999"),
        ("vps", "CLPDATA", "081295221639", "", "777999", "vps777999"),
        ("vps", "CLPDATA", "081295221639", "3040881", "", "vps777999"),
        ("vps", "CLPDATA", "081295221639", "3040881", "777999", ""),
    ],
)
def test_generate_signature_edge_empty(memberid, product, dest, refid, pin, password):
    service = OtomaxSignatureService()
    sig = service.generate_signature(memberid, product, dest, refid, pin, password)
    assert isinstance(sig, str)
    assert len(sig) > 0
