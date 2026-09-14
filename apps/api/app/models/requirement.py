from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPkMixin
from app.models.enums import Priority, RequirementStatus, RequirementType


class Requirement(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "requirements"
    __table_args__ = (UniqueConstraint("project_id", "code", name="uq_requirement_code"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    type: Mapped[RequirementType] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[Priority] = mapped_column(default=Priority.MEDIUM, nullable=False)
    status: Mapped[RequirementStatus] = mapped_column(
        default=RequirementStatus.DRAFT, nullable=False
    )
    verifiable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(Text, nullable=True)
