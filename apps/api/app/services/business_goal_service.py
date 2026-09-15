import uuid

from app.models.business_goal import BusinessGoal
from app.repositories.business_goal_repository import BusinessGoalRepository
from app.schemas.business_goal import BusinessGoalCreate, BusinessGoalUpdate


class BusinessGoalService:
    def __init__(self, goals: BusinessGoalRepository) -> None:
        self._goals = goals

    async def list_business_goals(self, project_id: uuid.UUID) -> list[BusinessGoal]:
        return await self._goals.list_for_project(project_id)

    async def get_business_goal(
        self, *, project_id: uuid.UUID, goal_id: uuid.UUID
    ) -> BusinessGoal | None:
        return await self._goals.get(project_id=project_id, goal_id=goal_id)

    async def create_business_goal(
        self, *, project_id: uuid.UUID, payload: BusinessGoalCreate
    ) -> BusinessGoal:
        goal = BusinessGoal(
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
        )
        self._goals.add(goal)
        await self._goals.flush()
        return goal

    async def update_business_goal(
        self, *, project_id: uuid.UUID, goal_id: uuid.UUID, payload: BusinessGoalUpdate
    ) -> BusinessGoal | None:
        goal = await self._goals.get(project_id=project_id, goal_id=goal_id)
        if goal is None:
            return None

        if payload.title is not None:
            goal.title = payload.title
        if payload.description is not None:
            goal.description = payload.description
        if payload.priority is not None:
            goal.priority = payload.priority

        await self._goals.flush()
        return goal

    async def delete_business_goal(self, *, project_id: uuid.UUID, goal_id: uuid.UUID) -> bool:
        goal = await self._goals.get(project_id=project_id, goal_id=goal_id)
        if goal is None:
            return False
        await self._goals.delete(goal)
        await self._goals.flush()
        return True
