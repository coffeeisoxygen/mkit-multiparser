"""Base Query Model Shared Schemas."""

from pydantic import BaseModel, Field, model_validator


class MemberTrxReqBase(BaseModel):
    memberid: str = Field(..., title="Member ID", description="The ID of the member")
    product: str = Field(
        ..., title="Product", description="The product being requested"
    )
    dest: str = Field(..., title="Destination", description="The destination number")
    refid: str = Field(..., title="Reference ID", description="The reference ID")


class MemberTrxWithSign(MemberTrxReqBase):
    sign: str = Field(
        ..., title="Signature", description="The signature for the transaction"
    )


class MemberTrxNoSign(MemberTrxReqBase):
    pin: str = Field(..., title="PIN", description="The PIN for the transaction")
    password: str = Field(
        ..., title="Password", description="The password for the transaction"
    )


class MemberTrxRequestAutoDetect(MemberTrxReqBase):
    sign: str | None = None
    pin: str | None = None
    password: str | None = None

    @model_validator(mode="before")
    def detect_and_validate_auth(cls, values):
        has_sign = bool(values.get("sign"))
        has_pinpass = bool(values.get("pin") and values.get("password"))
        if has_sign and has_pinpass:
            raise ValueError(
                "Tidak boleh mengirim sign dan pin/password sekaligus. Pilih salah satu metode autentikasi."
            )
        return values
