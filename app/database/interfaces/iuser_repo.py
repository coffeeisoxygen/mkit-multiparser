from abc import abstractmethod

from app.database.interfaces.base_interface import IRepository
from app.models.db_user import User as Db_User


class IUserRepository(IRepository[Db_User]):
    """Interface khusus user, extend CRUD dengan query spesifik."""

    @abstractmethod
    async def get_by_username(self, username: str) -> Db_User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Db_User | None: ...
