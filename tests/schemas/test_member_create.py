# """Unit test for MemberCreate schema validation."""

# # ruff : noqa
# # pyright: reportArgumentType = false
# import pytest
# from app.schemas.member.sch_member import MemberCreate
# from pydantic import AnyHttpUrl, ValidationError


# def test_member_create_valid():
#     member = MemberCreate(
#         memberid="M12345",
#         name="John Doe",
#         pin="123456",
#         password="Password90",  # valid: alphanumeric, >=8 chars
#         is_active=True,
#         ipaddress="192.168.1.1",
#         report_url=AnyHttpUrl("http://example.com/report"),
#         allow_nosign=False,
#     )
#     assert member.memberid == "M12345"
#     assert member.is_active is True
#     assert member.allow_nosign is False
#     assert member.pin == "123456"
#     assert member.password == "Password90"


# def test_member_create_invalid_pin():
#     with pytest.raises(ValidationError):
#         MemberCreate(
#             memberid="M12345",
#             name="John Doe",
#             pin="1234",  # too short
#             password="Password@90",
#             is_active=True,
#             ipaddress="192.168.1.1",
#             report_url="http://example.com/report",
#             allow_nosign=False,
#         )


# def test_member_create_invalid_password():
#     with pytest.raises(ValidationError):
#         MemberCreate(
#             memberid="M12345",
#             name="John Doe",
#             pin="123456",
#             password="pass word",  # whitespace not allowed
#             is_active=True,
#             ipaddress="192.168.1.1",
#             report_url="http://example.com/report",
#             allow_nosign=False,
#         )


# def test_member_create_invalid_ip():
#     with pytest.raises(ValidationError):
#         MemberCreate(
#             memberid="M12345",
#             name="John Doe",
#             pin="123456",
#             password="Password@90",
#             is_active=True,
#             ipaddress="not-an-ip",
#             report_url="http://example.com/report",
#             allow_nosign=False,
#         )


# def test_member_create_invalid_url():
#     with pytest.raises(ValidationError):
#         MemberCreate(
#             memberid="M12345",
#             name="John Doe",
#             pin="123456",
#             password="Password@90",
#             is_active=True,
#             ipaddress="192.168.1.1",
#             report_url="not-a-url",
#             allow_nosign=False,
#         )
