import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_project_role
from app.db.session import get_db
from app.models.project import ProjectRole
from app.repositories.business_goal_repository import BusinessGoalRepository
from app.schemas.business_goal import BusinessGoalCreate, BusinessGoalRead, BusinessGoalUpdate

router = APIRouter(prefix="/projects/{project_id}/business-goals", tags=["business-goals"])


def get_repo(db: AsyncSession = Depends(get_db)) -> BusinessGoalRepository:
    return BusinessGoalRepository(db)


@router.get(
    "",
    response_model=list[BusinessGoalRead],
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def list_business_goals(
    project_id: uuid.UUID, repo: BusinessGoalRepository = Depends(get_repo)
) -> list[BusinessGoalRead]:
    return await repo.list_for_project(project_id)  # type: ignore


@router.post(
    "",
    response_model=BusinessGoalRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def create_business_goal(
    project_id: uuid.UUID,
    payload: BusinessGoalCreate,
    db: AsyncSession = Depends(get_db),
    repo: BusinessGoalRepository = Depends(get_repo),
) -> BusinessGoalRead:
    goal = await repo.create(
        project_id=project_id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
    )
    await db.commit()
    return goal  # type: ignore


@router.patch(
    "/{goal_id}",
    response_model=BusinessGoalRead,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def update_business_goal(
    project_id: uuid.UUID,
    goal_id: uuid.UUID,
    payload: BusinessGoalUpdate,
    db: AsyncSession = Depends(get_db),
    repo: BusinessGoalRepository = Depends(get_repo),
) -> BusinessGoalRead:
    goal = await repo.get(project_id=project_id, goal_id=goal_id)
    if goal is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Business goal not found")

    if payload.title is not None:
        goal.title = payload.title
    if payload.description is not None:
        goal.description = payload.description
    if payload.priority is not None:
        goal.priority = payload.priority

    await repo.flush()
    await db.commit()

    return goal  # type: ignore


@router.delete(
    "/{goal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def delete_business_goal(
    project_id: uuid.UUID,
    goal_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    repo: BusinessGoalRepository = Depends(get_repo),
) -> None:
    goal = await repo.get(project_id=project_id, goal_id=goal_id)
    if goal is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Business goal not found")
    await repo.delete(goal)
    await db.commit()
