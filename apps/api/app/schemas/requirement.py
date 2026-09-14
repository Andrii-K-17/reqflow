import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import Priority, RequirementStatus, RequirementType


class RequirementCreate(BaseModel):
    type: RequirementType
    title: str = Field(min_length=1, max_length=500)
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    verifiable: bool = True
    rationale: str | None = None
    source: str | None = None


class RequirementUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = None
    priority: Priority | None = None
    status: RequirementStatus | None = None
    verifiable: bool | None = None
    rationale: str | None = None
    source: str | None = None


class RequirementRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    code: str
    type: RequirementType
    title: str
    description: str | None
    priority: Priority
    status: RequirementStatus
    verifiable: bool
    rationale: str | None
    source: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RequirementPage(BaseModel):
    items: list[RequirementRead]
    total: int
    page: int
    page_size: int
