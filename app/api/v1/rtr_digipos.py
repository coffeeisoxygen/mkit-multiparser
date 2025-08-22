from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter()


class DigiposQueryModel(BaseModel):
    """Model for DigiPos request data."""

    model_config = ConfigDict(
        title="DigiPosQueryModel",
        extra="forbid",
        json_schema_extra={"examples": [{"mod": "example_mod", "end": "example_end"}]},
    )
    mod: str = Field(description="moduleid sesuai setting")
    end: str = Field(description="endpoint sesuai setting")


@router.get(
    path="/trx",
    response_model=DigiposQueryModel,
    tags=["digipos"],
    summary="Forward request to DigiPos",
)
async def forward(
    req_model: Annotated[
        DigiposQueryModel,
        Query(
            json_schema_extra={"example": {"mod": "example_mod", "end": "example_end"}},
        ),
    ],
):
    return req_model
