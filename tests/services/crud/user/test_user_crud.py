import uuid

import pytest
from app.database.repositories.repo_user import UserRepo
from app.exception import UserDuplicateError, UserNotFoundError, UserPasswordError
from app.schemas.user.sch_user import UserCreate, UserUpdate, UserUpdatePassword
from app.services.crud.srv_user import UserService


@pytest.mark.asyncio
async def test_user_happy_path(db_session):
    """Test full user CRUD happy path."""
    repo = UserRepo()
    service = UserService(repo)

    # Create user
    data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        full_name="Test User",
        password="password123",
    )
    user = await service.create_user(db_session, data)
    assert user.username == data.username
    assert user.email == data.email
    assert user.full_name == data.full_name
    assert user.id is not None

    # Read user
    user_read = await service.get_user(db_session, user.id)
    assert user_read.username == data.username

    # Update profile
    update_data = UserUpdate(email="newemail@example.com", full_name="New Name")
    updated = await service.update_profile(db_session, user.id, update_data)
    assert updated.email == "newemail@example.com"
    assert updated.full_name == "New Name"

    # Update password
    pwd_data = UserUpdatePassword(
        old_password="password123",
        new_password="newpass456",
        confirm_password="newpass456",
        email=None,
        full_name=None,
    )
    updated_pwd = await service.update_password(db_session, user.id, pwd_data)
    assert updated_pwd.id == user.id

    # Soft delete
    deleted = await service.soft_delete(db_session, user.id)
    assert deleted.deleted_at is not None
    assert deleted.id == user.id

    # Restore
    restored = await service.restore(db_session, user.id)
    assert restored.deleted_at is None
    assert restored.is_active is True

    # Deactivate
    deactivated = await service.deactivate(db_session, user.id)
    assert deactivated.is_active is False

    # Activate
    activated = await service.activate(db_session, user.id)
    assert activated.is_active is True


@pytest.mark.asyncio
async def test_user_duplicate(db_session):
    """Test duplicate user creation raises error."""
    repo = UserRepo()
    service = UserService(repo)
    data = UserCreate(
        username="dupeuser",
        email="dupeuser@example.com",
        full_name="Dupe User",
        password="password123",
    )
    await service.create_user(db_session, data)
    with pytest.raises(UserDuplicateError):
        await service.create_user(db_session, data)


@pytest.mark.asyncio
async def test_user_not_found(db_session):
    """Test get/update/delete on non-existent user raises error."""
    repo = UserRepo()
    service = UserService(repo)
    fake_id = uuid.uuid4()
    with pytest.raises(UserNotFoundError):
        await service.get_user(db_session, fake_id)
    with pytest.raises(UserNotFoundError):
        await service.update_profile(
            db_session, fake_id, UserUpdate(email="x", full_name="y")
        )
    with pytest.raises(UserNotFoundError):
        await service.update_password(
            db_session,
            fake_id,
            UserUpdatePassword(
                old_password="x",
                new_password="y",
                confirm_password="y",
                email=None,
                full_name=None,
            ),
        )
    with pytest.raises(UserNotFoundError):
        await service.soft_delete(db_session, fake_id)
    with pytest.raises(UserNotFoundError):
        await service.restore(db_session, fake_id)
    with pytest.raises(UserNotFoundError):
        await service.activate(db_session, fake_id)
    with pytest.raises(UserNotFoundError):
        await service.deactivate(db_session, fake_id)


@pytest.mark.asyncio
async def test_user_password_error(db_session):
    """Test password update error cases."""
    repo = UserRepo()
    service = UserService(repo)
    data = UserCreate(
        username="pwduser",
        email="pwduser@example.com",
        full_name="Pwd User",
        password="oldpass",
    )
    user = await service.create_user(db_session, data)

    # Wrong old password
    pwd_data = UserUpdatePassword(
        old_password="wrongpass",
        new_password="newpass",
        confirm_password="newpass",
        email=None,
        full_name=None,
    )
    with pytest.raises(UserPasswordError):
        await service.update_password(db_session, user.id, pwd_data)

    # Mismatched new password confirmation
    pwd_data2 = UserUpdatePassword(
        old_password="oldpass",
        new_password="newpass",
        confirm_password="notmatch",
        email=None,
        full_name=None,
    )
    with pytest.raises(UserPasswordError):
        await service.update_password(db_session, user.id, pwd_data2)
