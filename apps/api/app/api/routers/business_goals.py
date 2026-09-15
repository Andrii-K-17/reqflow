import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_project_role
from app.db.session import get_db
from app.models.project import ProjectRole
from app.repositories.business_goal_repository import BusinessGoalRepository
from app.schemas.business_goal import BusinessGoalCreate, BusinessGoalRead, BusinessGoalUpdate
from app.services.business_goal_service import BusinessGoalService

router = APIRouter(prefix="/projects/{project_id}/business-goals", tags=["business-goals"])


def get_service(db: AsyncSession = Depends(get_db)) -> BusinessGoalService:
    return BusinessGoalService(BusinessGoalRepository(db))


@router.get(
    "",
    response_model=list[BusinessGoalRead],
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def list_business_goals(
    project_id: uuid.UUID, service: BusinessGoalService = Depends(get_service)
) -> list[BusinessGoalRead]:
    return await service.list_business_goals(project_id)  # type: ignore


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
    service: BusinessGoalService = Depends(get_service),
) -> BusinessGoalRead:
    goal = await service.create_business_goal(project_id=project_id, payload=payload)
    await db.commit()
    await db.refresh(goal)
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
    service: BusinessGoalService = Depends(get_service),
) -> BusinessGoalRead:
    goal = await service.update_business_goal(
        project_id=project_id, goal_id=goal_id, payload=payload
    )
    if goal is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Business goal not found")
    await db.commit()
    await db.refresh(goal)

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
    service: BusinessGoalService = Depends(get_service),
) -> None:
    deleted = await service.delete_business_goal(project_id=project_id, goal_id=goal_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Business goal not found")
    await db.commit()
