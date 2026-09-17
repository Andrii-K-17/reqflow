from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPkMixin
from app.models.enums import DiagramType


class Diagram(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "diagrams"
    __table_args__ = (UniqueConstraint("project_id", "code", name="uq_diagram_code"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[DiagramType] = mapped_column(nullable=False)
    mermaid_source: Mapped[str] = mapped_column(Text, nullable=False, default="")
