import pytest
from app.database.repositories.repo_user import UserRepository
from app.schemas import UserCreate, UserUpdate


# ruff:noqa
# pyright: reportArgumentType = false
# ---------- MOCK TEST ----------
class DummySession:
    def __init__(self):
        self._db = {}
        self._last_id = 0

    async def get(self, model, user_id):
        # match SQLAlchemy signature, ignore model
        return self._db.get(user_id)

    def add(self, obj):
        self._db[obj.id] = obj

    async def flush(self):
        pass

    async def execute(self, stmt):
        # Only support select by username/email for mock
        for user in self._db.values():
            if hasattr(stmt, "where"):
                if hasattr(stmt, "username") and user.username == stmt.username:
                    return DummyResult(user)
                if hasattr(stmt, "email") and user.email == stmt.email:
                    return DummyResult(user)
        return DummyResult(None)

    async def delete(self, obj):
        self._db.pop(obj.id, None)


class DummyResult:
    def __init__(self, user):
        self._user = user

    def scalar_one_or_none(self):
        return self._user

    def scalars(self):
        return DummyScalars([self._user] if self._user else [])

    def all(self):
        return [self._user] if self._user else []


class DummyScalars:
    def __init__(self, users):
        self._users = users

    def all(self):
        return self._users


@pytest.fixture
def mock_session():
    return DummySession()


@pytest.mark.asyncio
async def test_create_and_get_user_mock(mock_session):
    repo = UserRepository(mock_session)
    user_in = UserCreate(
        username="mockuser",
        email="mock@example.com",
        password="mockpass",  # >=6 chars
        full_name="MockUser",  # valid pattern
    )
    user = await repo.create_user(user_in)
    assert user.username == "mockuser"
    fetched = await repo.get_user_with_id(user.id)
    assert fetched is not None and fetched.username == "mockuser"


# ---------- IN-MEMORY DB TEST ----------
@pytest.mark.asyncio
async def test_create_and_get_user_db(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreate(
        username="dbuser",
        email="db@example.com",
        password="dbpass123",  # >=6 chars
        full_name="DBUser",  # valid pattern
    )
    user = await repo.create_user(user_in)
    assert user.username == "dbuser"
    fetched = await repo.get_user_with_id(user.id)
    assert fetched is not None and fetched.username == "dbuser"


@pytest.mark.asyncio
async def test_update_user_db(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreate(
        username="updateuser",
        email="update@example.com",
        password="updatepass",  # >=6 chars
        full_name="UpdateUser",  # valid pattern
    )
    user = await repo.create_user(user_in)
    update_in = UserUpdate(email="updated@example.com", full_name="Updated User")
    updated = await repo.update_user(user.id, update_in)
    assert updated is not None and updated.email == "updated@example.com"
    assert updated is not None and updated.full_name == "Updated User"


@pytest.mark.asyncio
async def test_delete_user_db(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreate(
        username="deluser",
        email="del@example.com",
        password="delpass",  # >=6 chars
        full_name="DelUser",  # valid pattern
    )
    user = await repo.create_user(user_in)
    result = await repo.delete_user(user.id)
    assert result is True
    assert await repo.get_user_with_id(user.id) is None


@pytest.mark.asyncio
async def test_soft_delete_and_restore_user_db(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreate(
        username="softuser",
        email="soft@example.com",
        password="softpass",  # >=6 chars
        full_name="SoftUser",  # valid pattern
    )
    user = await repo.create_user(user_in)
    soft_deleted = await repo.soft_delete_user(user.id)
    assert soft_deleted is not None and soft_deleted.is_active is False
    restored = await repo.restore_user(user.id)
    assert restored is not None and restored.is_active is True


@pytest.mark.asyncio
async def test_activate_deactivate_user_db(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreate(
        username="actuser",
        email="act@example.com",
        password="actpass",  # >=6 chars
        full_name="ActUser",  # valid pattern
    )
    user = await repo.create_user(user_in)
    deactivated = await repo.deactivate_user(user.id)
    assert deactivated is not None and deactivated.is_active is False
    activated = await repo.activate_user(user.id)
    assert activated is not None and activated.is_active is True


# ---------- EXTENDED COVERAGE ----------


@pytest.mark.asyncio
async def test_change_password_and_edge(db_session):
    repo = UserRepository(db_session)
    user_in = UserCreate(
        username="changepass",
        email="changepass@example.com",
        password="oldpass",  # >=6 chars
        full_name="ChangePass",  # valid pattern
    )
    user = await repo.create_user(user_in)
    result = await repo.change_password(user.id, "newpass")
    assert result is True
    # Edge: user not found
    result_none = await repo.change_password("notfound", "x")
    assert result_none is False


@pytest.mark.asyncio
async def test_set_unset_superuser_and_get_superusers(db_session):
    repo = UserRepository(db_session)
    # Create normal user
    user_in = UserCreate(
        username="normal",
        email="normal@example.com",
        password="normalpass",  # >=6 chars
        full_name="NormalUser",  # valid pattern
    )
    user = await repo.create_user(user_in)
    # Set superuser
    su = await repo.set_superuser(user.id)
    assert su is not None and su.is_superuser is True
    # Unset superuser
    su2 = await repo.unset_superuser(user.id)
    assert su2 is not None and su2.is_superuser is False
    # Get superusers
    await repo.set_superuser(user.id)
    su_list = await repo.get_superusers()
    assert any(u.id == user.id for u in su_list)
    # Edge: user not found
    assert await repo.set_superuser("notfound") is None
    assert await repo.unset_superuser("notfound") is None


@pytest.mark.asyncio
async def test_get_soft_deleted_users(db_session):
    repo = UserRepository(db_session)
    # Create and soft delete
    user_in = UserCreate(
        username="softdel",
        email="softdel@example.com",
        password="softdelpass",  # >=6 chars
        full_name="SoftDel",  # valid pattern
    )
    user = await repo.create_user(user_in)
    await repo.soft_delete_user(user.id)
    users = await repo.get_soft_deleted_users()
    assert users is not None and any(u.id == user.id for u in users)


@pytest.mark.asyncio
async def test_get_users_by_filter(db_session):
    repo = UserRepository(db_session)
    # Create users
    for i in range(3):
        await repo.create_user(
            UserCreate(
                username=f"filter{i}",
                email=f"filter{i}@ex.com",
                password="filterpass",  # >=6 chars
                full_name=f"Filter {chr(65 + i)}",  # valid pattern, e.g. "Filter A"
            )
        )
    # Filter by username
    users = await repo.get_users_by_filter({"username": "filter1"})
    assert users is not None and len(users) == 1 and users[0].username == "filter1"
    # Filter by non-existent field
    users_none = await repo.get_users_by_filter({"notafield": "x"})
    assert isinstance(users_none, list)


@pytest.mark.asyncio
async def test_count_users(db_session):
    repo = UserRepository(db_session)
    # Create active/inactive users
    ids = []
    for i in range(2):
        u = await repo.create_user(
            UserCreate(
                username=f"count{i}",
                email=f"count{i}@ex.com",
                password="countpass",  # >=6 chars
                full_name=f"Count {chr(65 + i)}",  # valid pattern, e.g. "Count A"
            )
        )
        ids.append(u.id)
    await repo.deactivate_user(ids[0])
    total = await repo.count_users()
    active = await repo.count_users(is_active=True)
    inactive = await repo.count_users(is_active=False)
    assert total >= 2
    assert active >= 1
    assert inactive >= 1
