"""Dependency factory untuk utility/general (hasher, dll).

Pisahkan dari repo/service agar lebih rapi dan maintainable.
"""

from app.utils.hasher.argon_hasher import Argon2Hasher
from app.utils.hasher.interface import HasherInterface


def get_hasher() -> HasherInterface:
    """Dependency untuk inject Argon2Hasher.

    Returns:
        HasherInterface: Instance Argon2Hasher.
    """
    return Argon2Hasher()


# Tambahkan factory utility lain di sini jika diperlukan
