from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPkMixin
from app.models.enums import TraceEntityType, TraceRelation


class TraceLink(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "trace_links"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "from_type",
            "from_id",
            "to_type",
            "to_id",
            "relation",
            name="uq_trace_link",
        ),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_type: Mapped[TraceEntityType] = mapped_column(nullable=False)
    from_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    to_type: Mapped[TraceEntityType] = mapped_column(nullable=False)
    to_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    relation: Mapped[TraceRelation] = mapped_column(nullable=False)
