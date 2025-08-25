import pytest
from app.utils.signature.impl_siganture import OtomaxSignatureService


@pytest.fixture
def signature_service():
    return OtomaxSignatureService()


def test_generate_signature_is_consistent(signature_service):
    # Arrange
    params = {
        "memberid": "abc123",
        "product": "pulsa",
        "dest": "08123456789",
        "refid": "REF001",
        "pin": "1234",
        "password": "secret",
    }
    # Act
    sig1 = signature_service.generate_signature(**params)
    sig2 = signature_service.generate_signature(**params)
    # Assert
    assert isinstance(sig1, str)
    assert sig1 == sig2


def test_generate_signature_differs_on_input(signature_service):
    # Arrange
    params1 = {
        "memberid": "abc123",
        "product": "pulsa",
        "dest": "08123456789",
        "refid": "REF001",
        "pin": "1234",
        "password": "secret",
    }
    params2 = params1.copy()
    params2["refid"] = "REF002"
    # Act
    sig1 = signature_service.generate_signature(**params1)
    sig2 = signature_service.generate_signature(**params2)
    # Assert
    assert sig1 != sig2


def test_verify_signature_success(signature_service):
    # Arrange
    params = {
        "memberid": "abc123",
        "product": "pulsa",
        "dest": "08123456789",
        "refid": "REF001",
        "pin": "1234",
        "password": "secret",
    }
    signature = signature_service.generate_signature(**params)
    # Act
    result = signature_service.verify_signature(signature, **params)
    # Assert
    assert result is True


def test_verify_signature_failure(signature_service):
    # Arrange
    params = {
        "memberid": "abc123",
        "product": "pulsa",
        "dest": "08123456789",
        "refid": "REF001",
        "pin": "1234",
        "password": "secret",
    }
    wrong_signature = "invalidsignature"
    # Act
    result = signature_service.verify_signature(wrong_signature, **params)
    # Assert
    assert result is False


def test_verify_signature_with_wrong_params(signature_service):
    # Arrange
    params = {
        "memberid": "abc123",
        "product": "pulsa",
        "dest": "08123456789",
        "refid": "REF001",
        "pin": "1234",
        "password": "secret",
    }
    signature = signature_service.generate_signature(**params)
    wrong_params = params.copy()
    wrong_params["password"] = "wrongpass"
    # Act
    result = signature_service.verify_signature(signature, **wrong_params)
    # Assert
    assert result is False
    assert result is False
