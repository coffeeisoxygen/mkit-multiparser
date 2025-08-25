# """Tests for ISessionRepository protocol contract.

# This test ensures that any implementation of ISessionRepository
# provides all required methods and expected signatures.
# """

# from unittest.mock import AsyncMock

# import pytest
# from app.database.repositories.intf_session import ISessionRepository
# from app.models import Session
# from app.schemas import SessionCreate


# class DummySessionRepository(ISessionRepository):
#     """Dummy implementation for protocol contract testing."""

#     async def get_session(self, session_id: int) -> Session | None:
#         return None

#     async def get_sessions_by_user(self, user_id: str) -> list[Session]:
#         return []

#     async def create_session(self, session_in: SessionCreate) -> Session:
#         return AsyncMock(spec=Session)()

#     async def delete_session(self, session_id: int) -> bool:
#         return True

#     async def delete_all_user_sessions(self, user_id: str) -> int:
#         return 0

#     async def activate_session(self, session_id: int) -> bool:
#         return True

#     async def deactivate_session(self, session_id: int) -> bool:
#         return True

#     async def get_active_sessions(self, user_id: str) -> list[Session]:
#         return []

#     async def purge_expired_sessions(self) -> int:
#         return 0

#     async def update_session_activity(
#         self, session_id: int, ip_address: str, user_agent: str
#     ) -> bool:
#         return True


# @pytest.mark.asyncio
# async def test_protocol_methods_exist():
#     """Ensure DummySessionRepository implements all protocol methods."""
#     repo = DummySessionRepository()
#     assert await repo.get_session(1) is None
#     assert await repo.get_sessions_by_user("user") == []
#     assert await repo.create_session(AsyncMock(spec=SessionCreate)()) is not None
#     assert await repo.delete_session(1) is True
#     assert await repo.delete_all_user_sessions("user") == 0
#     assert await repo.activate_session(1) is True
#     assert await repo.deactivate_session(1) is True
#     assert await repo.get_active_sessions("user") == []
#     assert await repo.purge_expired_sessions() == 0
#     assert await repo.update_session_activity(1, "127.0.0.1", "agent") is True
