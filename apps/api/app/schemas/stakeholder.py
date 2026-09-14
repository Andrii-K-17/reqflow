import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import StakeholderCategory


class StakeholderCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    category: StakeholderCategory = StakeholderCategory.PRIMARY
    interest_description: str | None = None


class StakeholderUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    category: StakeholderCategory | None = None
    interest_description: str | None = None


class StakeholderRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    category: StakeholderCategory
    interest_description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
