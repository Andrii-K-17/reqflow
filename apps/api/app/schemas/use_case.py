import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AlternativeFlow(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    condition: str = Field(min_length=1)
    steps: list[str] = Field(default_factory=list)


class UseCaseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    actors: list[str] = Field(default_factory=list)
    preconditions: str | None = None
    postconditions: str | None = None
    main_flow: list[str] = Field(default_factory=list)
    alternative_flows: list[AlternativeFlow] = Field(default_factory=list)


class UseCaseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    actors: list[str] | None = None
    preconditions: str | None = None
    postconditions: str | None = None
    main_flow: list[str] | None = None
    alternative_flows: list[AlternativeFlow] | None = None


class UseCaseRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    code: str
    title: str
    actors: list[str]
    preconditions: str | None
    postconditions: str | None
    main_flow: list[str]
    alternative_flows: list[AlternativeFlow]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
