import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business_goal import BusinessGoal


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

    def add(self, goal: BusinessGoal) -> None:
        self._session.add(goal)

    async def delete(self, goal: BusinessGoal) -> None:
        await self._session.delete(goal)

    async def flush(self) -> None:
        await self._session.flush()
