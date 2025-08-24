"""Test activate_user and deactivate_user CRUD functions."""

import pytest
from app.crud.crd_user import activate_user, create_user, deactivate_user
from app.models import User
from app.schemas import UserCreate
from sqlalchemy import delete


@pytest.mark.asyncio
async def test_activate_user_success(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="inactiveuser",
        email="inactive@example.com",
        full_name="Inactive User",
        password="pwact",
    )
    created = await create_user(db_session, user_data)
    # Set user nonaktif dulu
    await deactivate_user(db_session, created.id)
    result = await activate_user(db_session, created.id)
    db_user = await db_session.get(User, str(result.id))
    assert db_user.is_active is True


@pytest.mark.asyncio
async def test_deactivate_user_success(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="activeuser",
        email="active@example.com",
        full_name="Active User",
        password="pwdeact",
    )
    created = await create_user(db_session, user_data)
    result = await deactivate_user(db_session, created.id)
    db_user = await db_session.get(User, str(result.id))
    assert db_user.is_active is False
