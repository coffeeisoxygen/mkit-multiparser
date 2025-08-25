"""Dependency factory untuk utility/general (hasher, dll).

Pisahkan dari repo/service agar lebih rapi dan maintainable.
"""

from fastapi import Request

from app.utils.hasher.argon_hasher import Argon2Hasher
from app.utils.hasher.interface import HasherInterface


def get_hasher() -> HasherInterface:
    """Dependency untuk inject Argon2Hasher.

    Returns:
        HasherInterface: Instance Argon2Hasher.
    """
    return Argon2Hasher()


def get_request_context(request: Request) -> dict:
    """Ambil info kontekstual dari request (ip, user agent, headers)."""
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    return {
        "client_ip": client_ip,
        "user_agent": user_agent,
        "headers": dict(request.headers),
    }
