"""Unit test for MemberRepository: data loading, lookup, and edge cases."""

import tempfile
from pathlib import Path

import pytest
from app.exception.exceptions import FileDataIndexInUseError, FileDataNotFoundError
from app.repositories.rep_member import MemberRepository

SAMPLE_YAML = """
members:
  - memberid: M12345
    name: John Doe
    pin: "123456"
    password: "Password90"
    is_active: true
    ipaddress: "192.168.1.1"
    report_url: "http://example.com/report"
    allow_nosign: false
  - memberid: M54321
    name: Jane Smith
    pin: "654321"
    password: "Password99"
    is_active: false
    ipaddress: "192.168.1.2"
    report_url: "http://example.com/report2"
    allow_nosign: true
"""


def test_member_repository_load_and_lookup():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text(SAMPLE_YAML, encoding="utf-8")
        repo = MemberRepository(yaml_path)
        assert repo.get_member_count() == 2
        assert repo.has_member("M12345")
        assert repo.has_member("M54321")
        member = repo.get_member_by_id("M12345")
        assert member is not None
        assert member.name == "John Doe"
        assert repo.is_member_active("M12345") is True
        assert repo.is_member_active("M54321") is False
        assert repo.check_allow_nosign("M54321") is True
        assert repo.check_allow_nosign("M12345") is False
        ids = repo.get_member_ids()
        assert set(ids) == {"M12345", "M54321"}
        all_members = repo.get_all_members()
        assert len(all_members) == 2
        repo.clear_data()
        assert repo.get_member_count() == 0


def test_member_repository_file_not_found():
    fake_path = Path("/tmp/nonexistent.yaml")
    with pytest.raises(FileDataNotFoundError):
        MemberRepository(fake_path)


def test_member_repository_reload_fallback():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text(SAMPLE_YAML, encoding="utf-8")
        repo = MemberRepository(yaml_path)
        # Simulate file missing after initial load
        yaml_path.unlink()
        # Should fallback and keep old data
        repo.reload()
        assert repo.get_member_count() == 2


def test_member_repository_invalid_yaml():
    yaml_content = "members: [invalid: [unclosed"
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")
        with pytest.raises(FileDataIndexInUseError):
            MemberRepository(yaml_path)
