from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPkMixin


class UseCase(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "use_cases"
    __table_args__ = (UniqueConstraint("project_id", "code", name="uq_use_case_code"),)

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    actors: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    preconditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    postconditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    main_flow: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    alternative_flows: Mapped[list[dict]] = mapped_column(JSONB, default=list, nullable=False)
