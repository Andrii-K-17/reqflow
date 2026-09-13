from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPkMixin
from app.models.enums import StakeholderCategory


class Stakeholder(UUIDPkMixin, TimestampMixin, Base):
    __tablename__ = "stakeholders"

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[StakeholderCategory] = mapped_column(
        default=StakeholderCategory.PRIMARY, nullable=False
    )
    interest_description: Mapped[str | None] = mapped_column(Text, nullable=True)
