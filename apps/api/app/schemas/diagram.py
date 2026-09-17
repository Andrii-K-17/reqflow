import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import DiagramType


class DiagramCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    type: DiagramType
    mermaid_source: str = ""


class DiagramUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    mermaid_source: str | None = None


class DiagramRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    code: str
    title: str
    type: DiagramType
    mermaid_source: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
