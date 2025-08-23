"""Member Repository.

Repository pattern for member data management:
- Constructor injection with optional file path
- Delegates loading tasks to pure functions in srv_memberdata
- Public interface for data access
- Error handling with fallback behavior
- Integration with FileWatcher via reload callback
"""

from pathlib import Path

from loguru import logger

from app.schemas import MemberCreate
from app.utils import YamlDataUploader


class MemberRepository:
    """Repository for member data with fallback behavior and clean interface."""

    def __init__(self, file_path: Path | str):
        """Initialize MemberRepository."""
        self.file_path = Path(file_path)
        self.loader = YamlDataUploader("members", "memberid", MemberCreate, logger)
        self._members: list[MemberCreate] = []
        self._members_dict: dict[str, MemberCreate] = {}

        logger.info("Initializing MemberRepository", path=self.file_path)
        try:
            self.reload(initial=True)
        except Exception:
            # Propagate custom exceptions during initial load
            raise

    def _load_data_from_file(self) -> list[MemberCreate]:
        """Load data using YamlDataUploader.

        Returns:
            List of validated MemberInDB objects or empty list if file is empty.

        Raises:
            FileNotFoundError: If YAML file doesn't exist
            ValueError: If YAML structure is invalid or duplicates found
            ValidationError: If Pydantic validation fails
        """
        return self.loader.load_and_validate(self.file_path)

    def reload(self, initial: bool = False) -> None:
        """Reload all data from file and update internal state.

        Uses fallback behavior - if reload fails, keeps existing data and logs error.
        This ensures the repository remains functional even if file becomes temporarily invalid.
        If initial=True, propagate exceptions for testability.
        """
        logger.info("Starting MemberRepository reload")
        try:
            new_members = self._load_data_from_file()

            # Update both list and dict storage
            self._members = new_members
            self._members_dict = {m.memberid: m for m in new_members}

            logger.info(
                "MemberRepository reload completed successfully", count=len(new_members)
            )

        except Exception as e:
            if initial or not self._members:
                logger.error(
                    "Member data file not found or invalid during initial load",
                    error=str(e),
                    path=str(self.file_path),
                )
                raise
            logger.error(
                "Failed to reload member data, keeping existing data",
                error=str(e),
                current_count=len(self._members),
            )

    def get_member_by_id(self, memberid: str) -> MemberCreate | None:
        """Get member by ID with O(1) lookup."""
        member = self._members_dict.get(memberid)
        if member:
            logger.debug("Member found", memberid=memberid)
        else:
            logger.debug("Member not found", memberid=memberid)
        return member

    def get_all_members(self) -> list[MemberCreate]:
        """Get all members as a copy of the internal list."""
        return self._members.copy()

    def get_member_count(self) -> int:
        """Get total number of members."""
        return len(self._members)

    def is_member_active(self, memberid: str) -> bool:
        """Quick check if member exists and is active."""
        member = self.get_member_by_id(memberid)
        return member is not None and member.is_active

    def check_allow_nosign(self, memberid: str) -> bool:
        """Check if member allows authentication without signature."""
        member = self.get_member_by_id(memberid)
        return member is not None and member.allow_nosign

    def get_member_ids(self) -> list[str]:
        """Get all member IDs."""
        return list(self._members_dict.keys())

    def has_member(self, memberid: str) -> bool:
        """Check if member exists."""
        return memberid in self._members_dict

    def clear_data(self) -> None:
        """Clear all stored data (useful for testing)."""
        self._members.clear()
        self._members_dict.clear()
        logger.info("Member data cleared from repository")
