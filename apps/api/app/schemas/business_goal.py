import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import Priority


class BusinessGoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    priority: Priority = Priority.MEDIUM


class BusinessGoalUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    priority: Priority | None = None


class BusinessGoalRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    description: str | None
    priority: Priority
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
