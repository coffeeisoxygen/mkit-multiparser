# ruff: noqa

from app.database.core.session import get_db_session_manual_commit, get_db_transaction


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
