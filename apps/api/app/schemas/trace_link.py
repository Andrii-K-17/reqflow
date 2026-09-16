import uuid
from datetime import datetime

from pydantic import BaseModel, model_validator

from app.models.enums import TraceEntityType, TraceRelation


class TraceLinkCreate(BaseModel):
    from_type: TraceEntityType
    from_id: uuid.UUID
    to_type: TraceEntityType
    to_id: uuid.UUID
    relation: TraceRelation

    @model_validator(mode="after")
    def check_not_self_link(self) -> TraceLinkCreate:
        if self.from_type == self.to_type and self.from_id == self.to_id:
            raise ValueError("An entity cannot be linked to itself")
        return self


class TraceLinkRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    from_type: TraceEntityType
    from_id: uuid.UUID
    to_type: TraceEntityType
    to_id: uuid.UUID
    relation: TraceRelation
    created_at: datetime

    model_config = {"from_attributes": True}


class TraceGraphNode(BaseModel):
    id: uuid.UUID
    type: TraceEntityType
    code: str
    label: str


class TraceGraphEdge(BaseModel):
    from_id: uuid.UUID
    to_id: uuid.UUID
    relation: TraceRelation


class TraceGraph(BaseModel):
    nodes: list[TraceGraphNode]
    edges: list[TraceGraphEdge]
