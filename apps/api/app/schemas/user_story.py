import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserStoryCreate(BaseModel):
    role: str = Field(min_length=1, max_length=255)
    goal: str = Field(min_length=1)
    benefit: str = Field(min_length=1)
    acceptance_criteria: list[str] = Field(default_factory=list)


class UserStoryUpdate(BaseModel):
    role: str | None = Field(default=None, min_length=1, max_length=255)
    goal: str | None = Field(default=None, min_length=1)
    benefit: str | None = Field(default=None, min_length=1)
    acceptance_criteria: list[str] | None = None


class UserStoryRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    code: str
    role: str
    goal: str
    benefit: str
    acceptance_criteria: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
