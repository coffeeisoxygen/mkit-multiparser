"""schemas for member yg akan consume api ini."""

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    IPvAnyAddress,
    field_validator,
)


class MemberBase(BaseModel):
    memberid: str = Field(
        ..., description="ID unik untuk member", min_length=5, pattern=r"^[a-zA-Z0-9]*$"
    )
    name: str = Field(..., description="Nama member", min_length=1, max_length=100)
    ipaddress: IPvAnyAddress = Field(
        ..., alias="ipaddress", description="Alamat IP member"
    )
    report_url: AnyHttpUrl = Field(..., description="URL untuk laporan member")
    is_active: bool = Field(..., description="Status keaktifan member")
    allow_nosign: bool = Field(
        ...,
        description="Apakah member diizinkan untuk hit tanpa Signature.",
    )


class MemberCreate(MemberBase):
    """saat membuat member baru.

    saat loading Yaml / saat nanti ada actual db
    """

    model_config = ConfigDict(
        coerce_numbers_to_str=True,
        str_strip_whitespace=True,
        populate_by_name=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "memberid": "M12345",
                "name": "John Doe",
                "pin": "1234970",
                "password": "Password@90",
                "is_active": True,
                "ipaddress": "192.168.1.1",
                "report_url": "http://example.com/report",
                "allow_nosign": False,
            }
        },
    )

    pin: str = Field(
        description="PIN untuk member",
        min_length=6,
        max_length=6,
        pattern=r"^[0-9]+$",
    )
    password: str = Field(
        description="Password untuk member",
        min_length=8,
        max_length=100,
        pattern=r"^[a-zA-Z0-9]{8,100}$",  # at least 8 chars, only alphanumeric, no whitespace
    )

    @field_validator("is_active", "allow_nosign", mode="before")
    @classmethod
    def validate_is_active(cls, value: bool | None) -> bool:
        if not value:
            return False
        return value
