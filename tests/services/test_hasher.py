"""Test Argon2Hasher implementation."""

import pytest
from app.services.hasher.implement import Argon2Hasher

@pytest.mark.parametrize("password", ["password123", "rahasia!@#", "testPW"])
def test_hash_and_verify(password):
    hasher = Argon2Hasher()
    hashed = hasher.hash(password)
    assert isinstance(hashed, str)
    assert hasher.verify(password, hashed)
    assert not hasher.verify(password + "x", hashed)
