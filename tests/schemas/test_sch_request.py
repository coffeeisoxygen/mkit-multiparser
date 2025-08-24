"""Test untuk MemberTrxRequestAutoDetect schema fleksibel."""

import pytest
from app.schemas import MemberTrxRequest


def test_detect_signature_mode():
    data = {
        "memberid": "AKSES01",
        "product": "CLPDATA",
        "dest": "081295221639",
        "refid": "3042220LIST",
        "sign": "XmgNy8YxklljuM8lBsrMVnhX7uc",
    }
    model = MemberTrxRequest(**data)
    assert model.sign == "XmgNy8YxklljuM8lBsrMVnhX7uc"
    assert model.pin is None
    assert model.password is None


def test_detect_pin_password_mode():
    data = {
        "memberid": "AKSES01",
        "product": "CLPDATA",
        "dest": "081295221639",
        "refid": "3042220LIST",
        "pin": "777999",
        "password": "vps777999",
    }
    model = MemberTrxRequest(**data)
    assert model.sign is None
    assert model.pin == "777999"
    assert model.password == "vps777999"


def test_detect_missing_fields():
    data = {
        "memberid": "AKSES01",
        "product": "CLPDATA",
        "dest": "081295221639",
        "refid": "3042220LIST",
    }
    model = MemberTrxRequest(**data)
    assert model.sign is None
    assert model.pin is None
    assert model.password is None


def test_both_signmode_pinpassmode():
    data = {
        "memberid": "AKSES01",
        "product": "CLPDATA",
        "dest": "081295221639",
        "refid": "3042220LIST",
        "sign": "XmgNy8YxklljuM8lBsrMVnhX7uc",
        "pin": "777999",
        "password": "vps777999",
    }
    with pytest.raises(ValueError):
        MemberTrxRequest(**data)
