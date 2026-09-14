import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business_goal import BusinessGoal
from app.models.enums import Priority


class BusinessGoalRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_project(self, project_id: uuid.UUID) -> list[BusinessGoal]:
        stmt = (
            select(BusinessGoal)
            .where(BusinessGoal.project_id == project_id)
            .order_by(BusinessGoal.created_at)
        )
        result = await self._session.execute(stmt)

        return list(result.scalars().all())

    async def get(self, *, project_id: uuid.UUID, goal_id: uuid.UUID) -> BusinessGoal | None:
        stmt = select(BusinessGoal).where(
            BusinessGoal.id == goal_id, BusinessGoal.project_id == project_id
        )
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        project_id: uuid.UUID,
        title: str,
        description: str | None,
        priority: Priority,
    ) -> BusinessGoal:
        goal = BusinessGoal(
            project_id=project_id,
            title=title,
            description=description,
            priority=priority,
        )
        self._session.add(goal)
        await self._session.flush()

        return goal

    async def delete(self, goal: BusinessGoal) -> None:
        await self._session.delete(goal)
        await self._session.flush()

    async def flush(self) -> None:
        await self._session.flush()
