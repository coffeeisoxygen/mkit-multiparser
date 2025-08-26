from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")  # ORM entity type


class IRepository[T](ABC):
    """Base repository interface: CRUD dasar."""

    @abstractmethod
    async def create(self, obj_in: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, obj_id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, offset: int = 0, limit: int = 50) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, obj_id: int, obj_in: dict) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, obj_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, obj_id: int) -> bool:
        raise NotImplementedError
