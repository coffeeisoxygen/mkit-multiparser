"""Base Request Shared Schemas."""

from pydantic import BaseModel


class TransactionRequestSchema(BaseModel):
    trxid: str
    refid: str
    dest: str
    product: str
    memberid: str
