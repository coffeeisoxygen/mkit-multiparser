# ruff:noqa
import pytest
from app.database.repositories.intf_user import IUserRepository
from app.models.db_user import User
from app.schemas.user import UserCreate, UserUpdate


class MockUserRepository(IUserRepository):
    async def create_user(self, user_in: UserCreate) -> User:
        return User(id="1", username=user_in.username, email=user_in.email)

    async def get_user_with_id(self, user_id: int) -> User | None:
        return User(id=user_id, username="test", email="test@example.com")

    async def get_user_with_username(self, username: str) -> User | None:
        return User(id="1", username=username, email="test@example.com")

    async def get_user_with_email(self, email: str) -> User | None:
        return User(id="1", username="test", email=email)

    async def get_all_users(
        self, offset: int = 0, limit: int = 50, is_active: bool | None = None
    ) -> list[User]:
        return [User(id="1", username="test", email="test@example.com")]

    async def update_user(self, user_id: int, user_in: UserUpdate) -> User | None:
        # username tidak boleh diubah, hanya update field yang valid
        return User(
            id=user_id,
            username="test",  # tetap
            email=user_in.email or "test@example.com",
            full_name=user_in.full_name or "Test User",
        )

    async def delete_user(self, user_id: int) -> bool:
        return True

    async def soft_delete_user(self, user_id: int) -> User | None:
        return User(id=user_id, username="test", email="test@example.com")

    async def restore_user(self, user_id: int) -> User | None:
        return User(id=user_id, username="test", email="test@example.com")

    async def activate_user(self, user_id: int) -> User | None:
        return User(id=user_id, username="test", email="test@example.com")

    async def deactivate_user(self, user_id: int) -> User | None:
        return User(id=user_id, username="test", email="test@example.com")

    async def change_password(self, user_id: int, new_password: str) -> bool:
        return True

    async def set_superuser(self, user_id: int) -> User | None:
        return User(id=user_id, username="super", email="super@example.com")

    async def unset_superuser(self, user_id: int) -> User | None:
        return User(id=user_id, username="test", email="test@example.com")

    async def get_superusers(self, offset: int = 0, limit: int = 50) -> list[User]:
        return [User(id="1", username="super", email="super@example.com")]

    async def get_soft_deleted_users(
        self, offset: int = 0, limit: int = 50
    ) -> list[User]:
        return [User(id="2", username="deleted", email="deleted@example.com")]

    async def get_users_by_filter(
        self, filters: dict, offset: int = 0, limit: int = 50
    ) -> list[User]:
        return [User(id="1", username="filtered", email="filtered@example.com")]

    async def count_users(self, is_active: bool | None = None) -> int:
        return 1


@pytest.fixture
def repo():
    return MockUserRepository()


@pytest.mark.asyncio
async def test_create_user(repo):
    # Arrange
    user_in = UserCreate(
        username="newuser",
        email="new@example.com",
        password="pass123",  # minimal 6 karakter
        full_name="New User",
    )
    # Act
    user = await repo.create_user(user_in)
    # Assert
    assert user.username == "newuser"
    assert user.email == "new@example.com"


@pytest.mark.asyncio
async def test_get_user_with_id(repo):
    user = await repo.get_user_with_id("1")
    assert user.id == "1"


@pytest.mark.asyncio
async def test_get_user_with_username(repo):
    user = await repo.get_user_with_username("testuser")
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_get_user_with_email(repo):
    user = await repo.get_user_with_email("mail@example.com")
    assert user.email == "mail@example.com"


@pytest.mark.asyncio
async def test_get_all_users(repo):
    users = await repo.get_all_users()
    assert isinstance(users, list)
    assert users


@pytest.mark.asyncio
async def test_update_user(repo):
    user_in = UserUpdate(email="updated@example.com")
    user = await repo.update_user("1", user_in)
    assert user.email == "updated@example.com"


@pytest.mark.asyncio
async def test_delete_user(repo):
    result = await repo.delete_user("1")
    assert result is True


@pytest.mark.asyncio
async def test_soft_delete_user(repo):
    user = await repo.soft_delete_user("2")
    assert user.id == "2"


@pytest.mark.asyncio
async def test_restore_user(repo):
    user = await repo.restore_user("2")
    assert user.id == "2"


@pytest.mark.asyncio
async def test_activate_user(repo):
    user = await repo.activate_user("1")
    assert user.id == "1"


@pytest.mark.asyncio
async def test_deactivate_user(repo):
    user = await repo.deactivate_user("1")
    assert user.id == "1"


@pytest.mark.asyncio
async def test_change_password(repo):
    result = await repo.change_password("1", "newpass")
    assert result is True


@pytest.mark.asyncio
async def test_set_superuser(repo):
    user = await repo.set_superuser("1")
    assert user.username == "super"


@pytest.mark.asyncio
async def test_unset_superuser(repo):
    user = await repo.unset_superuser("1")
    assert user.username == "test"


@pytest.mark.asyncio
async def test_get_superusers(repo):
    users = await repo.get_superusers()
    assert users[0].username == "super"


@pytest.mark.asyncio
async def test_get_soft_deleted_users(repo):
    users = await repo.get_soft_deleted_users()
    assert users[0].username == "deleted"


@pytest.mark.asyncio
async def test_get_users_by_filter(repo):
    users = await repo.get_users_by_filter({"username": "filtered"})
    assert users[0].username == "filtered"


@pytest.mark.asyncio
async def test_count_users(repo):
    count = await repo.count_users()
    assert count == 1
