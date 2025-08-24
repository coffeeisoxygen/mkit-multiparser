"""Test create_user CRUD function and edge cases."""

import pytest
from app.crud.crd_user import create_user
from app.exception import UserDuplicateError
from app.models import User
from app.schemas import UserCreate
from app.services.hasher.implement import Argon2Hasher
from sqlalchemy import delete


@pytest.mark.asyncio
async def test_create_user_success(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()

    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        full_name="New User",
        password="mysecretpw",
    )
    result = await create_user(db_session, user_data)
    assert result.username == "newuser"
    assert result.email == "newuser@example.com"
    assert result.full_name == "New User"
    assert result.id is not None
    db_user = await db_session.get(User, str(result.id))
    hasher = Argon2Hasher()
    assert hasher.verify("mysecretpw", db_user.hashed_password)


@pytest.mark.asyncio
async def test_create_user_duplicate(db_session):
    await db_session.execute(delete(User))
    await db_session.commit()
    user_data = UserCreate(
        username="dupeuser",
        email="dupeuser@example.com",
        full_name="Dupe User",
        password="pw1",
    )
    await create_user(db_session, user_data)
    with pytest.raises(UserDuplicateError):
        await create_user(db_session, user_data)
