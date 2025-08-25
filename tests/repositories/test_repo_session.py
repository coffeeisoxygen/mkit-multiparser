import datetime
import uuid

import pytest
from app.database.repositories.repo_session import SessionRepository
from app.schemas.session.sch_session import SessionCreate


@pytest.mark.asyncio
async def test_create_and_get_session(db_session):
    repo = SessionRepository(db_session)
    session_in = SessionCreate(
        user_id=uuid.uuid4(),
        token="token1",
        ip_address="127.0.0.1",
        user_agent="pytest-agent",
    )
    session = await repo.create_session(session_in)
    assert str(session.user_id) == str(session_in.user_id)
    fetched = await repo.get_session(session.id)
    assert fetched is not None and str(fetched.user_id) == str(session_in.user_id)


@pytest.mark.asyncio
async def test_get_sessions_by_user(db_session):
    repo = SessionRepository(db_session)
    # Create two sessions for user2
    user_id = uuid.uuid4()
    for i in range(2):
        await repo.create_session(
            SessionCreate(
                user_id=user_id,
                token=f"token{i + 2}",
                ip_address=f"127.0.0.{i}",
                user_agent="pytest-agent",
            )
        )
    sessions = await repo.get_sessions_by_user(str(user_id))
    assert len(sessions) == 2


@pytest.mark.asyncio
async def test_delete_session_and_edge(db_session):
    repo = SessionRepository(db_session)
    user_id = uuid.uuid4()
    session_in = SessionCreate(
        user_id=user_id,
        token="token3",
        ip_address="127.0.0.3",
        user_agent="pytest-agent",
    )
    session = await repo.create_session(session_in)
    result = await repo.delete_session(session.id)
    assert result is True
    assert await repo.get_session(session.id) is None
    # Edge: session not found
    result_none = await repo.delete_session(99999)
    assert result_none is False


@pytest.mark.asyncio
async def test_delete_all_user_sessions(db_session):
    repo = SessionRepository(db_session)
    # Create sessions for user4
    user_id = uuid.uuid4()
    for i in range(3):
        await repo.create_session(
            SessionCreate(
                user_id=user_id,
                token=f"token4{i}",
                ip_address=f"127.0.0.{i}",
                user_agent="pytest-agent",
            )
        )
    deleted_count = await repo.delete_all_user_sessions(str(user_id))
    assert deleted_count == 3
    assert await repo.get_sessions_by_user(str(user_id)) == []


@pytest.mark.asyncio
async def test_activate_deactivate_session(db_session):
    repo = SessionRepository(db_session)
    user_id = uuid.uuid4()
    session_in = SessionCreate(
        user_id=user_id,
        token="token5",
        ip_address="127.0.0.5",
        user_agent="pytest-agent",
    )
    session = await repo.create_session(session_in)
    activated = await repo.activate_session(session.id)
    assert activated is True
    deactivated = await repo.deactivate_session(session.id)
    assert deactivated is True


@pytest.mark.asyncio
async def test_get_active_sessions(db_session):
    repo = SessionRepository(db_session)
    # Create active/inactive sessions for user6
    user_id = uuid.uuid4()
    active = await repo.create_session(
        SessionCreate(
            user_id=user_id,
            token="token6a",
            ip_address="127.0.0.6",
            user_agent="pytest-agent",
        )
    )
    inactive = await repo.create_session(
        SessionCreate(
            user_id=user_id,
            token="token6b",
            ip_address="127.0.0.7",
            user_agent="pytest-agent",
        )
    )
    active_sessions = await repo.get_active_sessions(str(user_id))
    assert any(s.id == active.id for s in active_sessions)
    assert all(s.is_active for s in active_sessions)


@pytest.mark.asyncio
async def test_purge_expired_sessions(db_session):
    repo = SessionRepository(db_session)
    user_id = uuid.uuid4()
    now = datetime.datetime.utcnow()
    # Create expired and valid sessions
    expired = await repo.create_session(
        SessionCreate(
            user_id=user_id,
            token="token7a",
            ip_address="127.0.0.8",
            user_agent="pytest-agent",
        )
    )
    valid = await repo.create_session(
        SessionCreate(
            user_id=user_id,
            token="token7b",
            ip_address="127.0.0.9",
            user_agent="pytest-agent",
        )
    )
    # Manually set expires_at for expired/valid
    expired.expires_at = now - datetime.timedelta(days=1)
    valid.expires_at = now + datetime.timedelta(days=1)
    await db_session.flush()
    purged = await repo.purge_expired_sessions()
    assert purged >= 1
    remaining = await repo.get_sessions_by_user(str(user_id))
    assert any(s.id == valid.id for s in remaining)
    assert all(s.expires_at > now for s in remaining)


@pytest.mark.asyncio
async def test_update_session_activity(db_session):
    repo = SessionRepository(db_session)
    user_id = uuid.uuid4()
    session_in = SessionCreate(
        user_id=user_id,
        token="token8",
        ip_address="127.0.0.10",
        user_agent="pytest-agent",
    )
    session = await repo.create_session(session_in)
    updated = await repo.update_session_activity(session.id, "192.168.1.1", "new-agent")
    assert updated is True
