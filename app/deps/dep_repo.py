"""Dependency factory untuk repository (user, session, dst).

Pisahkan dari service agar lebih rapi dan maintainable.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.intf_session import ISessionRepository
from app.database.repositories.intf_user import IUserRepository
from app.database.repositories.repo_session import SessionRepository
from app.database.repositories.repo_user import UserRepository
from app.deps.dep_database import get_session


def get_user_repo(
    session: AsyncSession = Depends(get_session),
) -> IUserRepository:
    """Dependency untuk inject UserRepository."""
    return UserRepository(session)


def get_session_repo(
    session: AsyncSession = Depends(get_session),
) -> ISessionRepository:
    """Dependency untuk inject SessionRepository."""
    return SessionRepository(session)
