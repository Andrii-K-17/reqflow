import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business_goal import BusinessGoal
from app.models.enums import TraceEntityType
from app.models.requirement import Requirement
from app.models.use_case import UseCase
from app.models.user_story import UserStory


@dataclass(frozen=True)
class EntityLabel:
    """Immutable display representation of a trace entity."""

    code: str
    label: str


class EntityResolver:
    """Resolves polymorphic trace entities against concrete database tables."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exists(
        self,
        *,
        project_id: uuid.UUID,
        entity_type: TraceEntityType,
        entity_id: uuid.UUID,
    ) -> bool:
        """Check if the entity exists within the given project."""
        return (
            await self._fetch(
                project_id=project_id,
                entity_type=entity_type,
                entity_id=entity_id,
            )
            is not None
        )

    async def resolve_label(
        self,
        *,
        project_id: uuid.UUID,
        entity_type: TraceEntityType,
        entity_id: uuid.UUID,
    ) -> EntityLabel | None:
        """Fetch entity and return its human-readable code and label."""
        entity = await self._fetch(
            project_id=project_id,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        if entity is None:
            return None

        if isinstance(entity, BusinessGoal):
            return EntityLabel(code="GOAL", label=entity.title)
        if isinstance(entity, Requirement):
            return EntityLabel(code=entity.code, label=entity.title)
        if isinstance(entity, UseCase):
            return EntityLabel(code=entity.code, label=entity.title)
        if isinstance(entity, UserStory):
            return EntityLabel(code=entity.code, label=f"{entity.role}: {entity.goal}")

        raise ValueError(f"Unknown entity type: {entity_type}")

    async def _fetch(
        self,
        *,
        project_id: uuid.UUID,
        entity_type: TraceEntityType,
        entity_id: uuid.UUID,
    ) -> BusinessGoal | Requirement | UseCase | UserStory | None:
        """Query the target entity by ID scoped to project_id."""
        model = {
            TraceEntityType.BUSINESS_GOAL: BusinessGoal,
            TraceEntityType.REQUIREMENT: Requirement,
            TraceEntityType.USE_CASE: UseCase,
            TraceEntityType.USER_STORY: UserStory,
        }[entity_type]

        stmt = select(model).where(model.id == entity_id, model.project_id == project_id)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()
