from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.core.session import get_db_session_manual_commit, get_db_transaction
from app.database.repositories.intf_session import ISessionRepository
from app.database.repositories.intf_user import IUserRepository
from app.database.repositories.repo_session import SessionRepository
from app.database.repositories.repo_user import UserRepository


async def get_session():
    """Dependency FastAPI untuk mendapatkan session database dengan Unit of Work pattern.

    Yields:
        AsyncSession: Session database yang siap digunakan untuk operasi ORM.
    """
    async with get_db_transaction() as session:
        yield session


async def get_session_manual():
    """Dependency FastAPI untuk mendapatkan session database dengan kontrol manual commit.

    Yields:
        AsyncSession: Session database yang membutuhkan commit/rollback manual.
    """
    async with get_db_session_manual_commit() as session:
        yield session


def get_user_repo(session: AsyncSession = Depends(get_session)) -> IUserRepository:
    return UserRepository(session)


def get_session_repo(
    session: AsyncSession = Depends(get_session),
) -> ISessionRepository:
    return SessionRepository(session)
