"""Test get_user and get_user_by_username CRUD functions, including soft delete filter."""

# pyright: reportOptionalMemberAccess = false
import uuid

import pytest
from app.crud.crd_user import (
    create_user,
    get_user,
    get_user_by_username,
    soft_delete_user,
)
from app.exception import UserNotFoundError
from app.models import User
from app.schemas import UserCreate
from sqlalchemy import delete


@pytest.mark.asyncio
async def test_get_user_found(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="getuser",
        email="getuser@example.com",
        full_name="Get User",
        password="pwget",
    )
    created = await create_user(db_session, user_data)
    result = await get_user(db_session, created.id)
    assert result.username == "getuser"
    assert result.email == "getuser@example.com"
    assert result.full_name == "Get User"
    assert result.id == created.id


@pytest.mark.asyncio
async def test_get_user_not_found(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    with pytest.raises(UserNotFoundError):
        await get_user(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_get_user_soft_deleted(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="softdeluser",
        email="softdeluser@example.com",
        full_name="Soft Del User",
        password="pwsoftdel",
    )
    created = await create_user(db_session, user_data)
    await soft_delete_user(db_session, created.id)
    with pytest.raises(UserNotFoundError):
        await get_user(db_session, created.id)


@pytest.mark.asyncio
async def test_get_user_by_username_found(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="byusername",
        email="byusername@example.com",
        full_name="By Username",
        password="pwbyusername",
    )
    created = await create_user(db_session, user_data)
    result = await get_user_by_username(db_session, "byusername")
    assert result.username == "byusername"
    assert result.email == "byusername@example.com"
    assert result.full_name == "By Username"
    assert result.id == created.id


@pytest.mark.asyncio
async def test_get_user_by_username_not_found(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    result = await get_user_by_username(db_session, "notfound")
    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_username_soft_deleted(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="softdelbyusername",
        email="softdelbyusername@example.com",
        full_name="Soft Del By Username",
        password="pwsoftdelbyusername",
    )
    created = await create_user(db_session, user_data)
    await soft_delete_user(db_session, created.id)
    result = await get_user_by_username(db_session, "softdelbyusername")
    assert result is None
