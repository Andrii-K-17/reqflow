import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.project import ProjectRole


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None


class ProjectRead(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    owner_id: uuid.UUID
    my_role: ProjectRole
    archived_at: datetime | None
    created_at: datetime
    updated_at: datetime
