"""Unit test for YamlDataUploader: load and validate member data from YAML."""

import tempfile
from pathlib import Path

import pytest
from app.exception.exceptions import (
    FileIndexInUseError,
    FileNotFoundError,
    FormatFileError,
)
from app.schemas.member.sch_member import MemberCreate
from app.utils.yaml_uploader import YamlDataUploader
from loguru import logger
from pydantic import ValidationError

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


def test_yaml_data_uploader_load_and_validate():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text(SAMPLE_YAML, encoding="utf-8")
        uploader = YamlDataUploader("members", "memberid", MemberCreate, logger)
        members = uploader.load_and_validate(yaml_path)
        assert len(members) == 2
        assert members[0].memberid == "M12345"
        assert members[1].allow_nosign is True


def test_yaml_data_uploader_duplicate():
    yaml_content = """
members:
  - memberid: M12345
    name: John Doe
    pin: "123456"
    password: "Password90"
    is_active: true
    ipaddress: "192.168.1.1"
    report_url: "http://example.com/report"
    allow_nosign: false
  - memberid: M12345
    name: Jane Smith
    pin: "654321"
    password: "Password99"
    is_active: false
    ipaddress: "192.168.1.2"
    report_url: "http://example.com/report2"
    allow_nosign: true
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")
        uploader = YamlDataUploader("members", "memberid", MemberCreate, logger)
        with pytest.raises(ValueError):
            uploader.load_and_validate(yaml_path)


def test_yaml_data_uploader_file_not_found():
    uploader = YamlDataUploader("members", "memberid", MemberCreate, logger)
    fake_path = Path("/tmp/nonexistent.yaml")
    with pytest.raises(FileNotFoundError):
        uploader.load_and_validate(fake_path)


def test_yaml_data_uploader_yaml_parse_error():
    yaml_content = "members: [invalid: [unclosed"
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")
        uploader = YamlDataUploader("members", "memberid", MemberCreate, logger)
        with pytest.raises(FormatFileError):
            uploader.load_and_validate(yaml_path)


def test_yaml_data_uploader_items_not_list():
    yaml_content = "members: {memberid: M12345, name: John}"
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")
        uploader = YamlDataUploader("members", "memberid", MemberCreate, logger)
        with pytest.raises(FileIndexInUseError):
            uploader.load_and_validate(yaml_path)


def test_yaml_data_uploader_missing_key():
    yaml_content = """
notmembers:
  - memberid: M12345
    name: John Doe
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")
        uploader = YamlDataUploader("members", "memberid", MemberCreate, logger)
        with pytest.raises(FileIndexInUseError):
            uploader.load_and_validate(yaml_path)


def test_yaml_data_uploader_model_validation_error():
    yaml_content = """
members:
  - memberid: M12345
    # missing required fields like name, pin, password, etc.
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text(yaml_content, encoding="utf-8")
        uploader = YamlDataUploader("members", "memberid", MemberCreate, logger)
        with pytest.raises(ValidationError):
            uploader.load_and_validate(yaml_path)


def test_yaml_data_uploader_empty_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = Path(tmpdir) / "members.yaml"
        yaml_path.write_text("", encoding="utf-8")
        uploader = YamlDataUploader("members", "memberid", MemberCreate, logger)
        with pytest.raises(FileIndexInUseError):
            uploader.load_and_validate(yaml_path)
