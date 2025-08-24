"""Test update_user_profile and update_user_password CRUD functions."""

import uuid

import pytest
from app.crud.crd_user import create_user, update_user_password, update_user_profile
from app.exception import UserNotFoundError, UserPasswordError
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserUpdatePassword
from sqlalchemy import delete


@pytest.mark.asyncio
async def test_update_user_profile_success(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="updateuser",
        email="updateuser@example.com",
        full_name="Update User",
        password="pwupdate",
    )
    created = await create_user(db_session, user_data)
    update_data = UserUpdate(email="updated@example.com", full_name="Updated Name")
    result = await update_user_profile(db_session, created.id, update_data)
    assert result.email == "updated@example.com"
    assert result.full_name == "Updated Name"


@pytest.mark.asyncio
async def test_update_user_profile_not_found(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    update_data = UserUpdate(email="x@example.com", full_name="X")
    with pytest.raises(UserNotFoundError):
        await update_user_profile(db_session, uuid.uuid4(), update_data)


@pytest.mark.asyncio
async def test_update_user_password_success(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="pwuser",
        email="pwuser@example.com",
        full_name="PW User",
        password="oldpw",
    )
    created = await create_user(db_session, user_data)
    update_pw = UserUpdatePassword(
        email=None,
        full_name=None,
        old_password="oldpw",
        new_password="newpw",
        confirm_password="newpw",
    )
    result = await update_user_password(db_session, created.id, update_pw)
    assert result.id == created.id


@pytest.mark.asyncio
async def test_update_user_password_wrong_old(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="wrongpwuser",
        email="wrongpwuser@example.com",
        full_name="Wrong PW User",
        password="oldpw",
    )
    created = await create_user(db_session, user_data)
    update_pw = UserUpdatePassword(
        email=None,
        full_name=None,
        old_password="wrongpw",
        new_password="newpw",
        confirm_password="newpw",
    )
    with pytest.raises(UserPasswordError):
        await update_user_password(db_session, created.id, update_pw)


@pytest.mark.asyncio
async def test_update_user_password_mismatch_confirm(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="mismatchpwuser",
        email="mismatchpwuser@example.com",
        full_name="Mismatch PW User",
        password="oldpw",
    )
    created = await create_user(db_session, user_data)
    update_pw = UserUpdatePassword(
        email=None,
        full_name=None,
        old_password="oldpw",
        new_password="newpw",
        confirm_password="wrongconfirm",
    )
    with pytest.raises(UserPasswordError):
        await update_user_password(db_session, created.id, update_pw)
