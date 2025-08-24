"""Test soft_delete_user and restore_user CRUD functions and edge cases."""

import pytest
from app.crud.crd_user import create_user, restore_user, soft_delete_user
from app.exception import UserNotFoundError
from app.models import User
from app.schemas import UserCreate
from sqlalchemy import delete


@pytest.mark.asyncio
async def test_soft_delete_user_success(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="deluser",
        email="deluser@example.com",
        full_name="Del User",
        password="pwdel",
    )
    created = await create_user(db_session, user_data)
    result = await soft_delete_user(db_session, created.id)
    db_user = await db_session.get(User, str(result.id))
    assert db_user.deleted_at is not None
    assert db_user.is_active is False


@pytest.mark.asyncio
async def test_restore_user_success(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="restoreuser",
        email="restoreuser@example.com",
        full_name="Restore User",
        password="pwrestore",
    )
    created = await create_user(db_session, user_data)
    await soft_delete_user(db_session, created.id)
    result = await restore_user(db_session, created.id)
    db_user = await db_session.get(User, str(result.id))
    assert db_user.deleted_at is None
    assert db_user.is_active is True


@pytest.mark.asyncio
async def test_restore_user_not_soft_deleted(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="notsoftdel",
        email="notsoftdel@example.com",
        full_name="Not Soft Del",
        password="pwnotsoft",
    )
    created = await create_user(db_session, user_data)
    with pytest.raises(UserNotFoundError):
        await restore_user(db_session, created.id)
