import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_project_role
from app.db.session import get_db
from app.models.project import ProjectRole
from app.repositories.stakeholder_repository import StakeholderRepository
from app.schemas.stakeholder import StakeholderCreate, StakeholderRead, StakeholderUpdate

router = APIRouter(prefix="/projects/{project_id}/stakeholders", tags=["stakeholders"])


def get_repo(db: AsyncSession = Depends(get_db)) -> StakeholderRepository:
    return StakeholderRepository(db)


@router.get(
    "",
    response_model=list[StakeholderRead],
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def list_stakeholders(
    project_id: uuid.UUID, repo: StakeholderRepository = Depends(get_repo)
) -> list[StakeholderRead]:
    return await repo.list_for_project(project_id)  # type: ignore


@router.post(
    "",
    response_model=StakeholderRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def create_stakeholder(
    project_id: uuid.UUID,
    payload: StakeholderCreate,
    db: AsyncSession = Depends(get_db),
    repo: StakeholderRepository = Depends(get_repo),
) -> StakeholderRead:
    stakeholder = await repo.create(
        project_id=project_id,
        name=payload.name,
        category=payload.category,
        interest_description=payload.interest_description,
    )
    await db.commit()
    return stakeholder  # type: ignore


@router.patch(
    "/{stakeholder_id}",
    response_model=StakeholderRead,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def update_stakeholder(
    project_id: uuid.UUID,
    stakeholder_id: uuid.UUID,
    payload: StakeholderUpdate,
    db: AsyncSession = Depends(get_db),
    repo: StakeholderRepository = Depends(get_repo),
) -> StakeholderRead:
    stakeholder = await repo.get(project_id=project_id, stakeholder_id=stakeholder_id)
    if stakeholder is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Stakeholder not found")

    if payload.name is not None:
        stakeholder.name = payload.name
    if payload.category is not None:
        stakeholder.category = payload.category
    if payload.interest_description is not None:
        stakeholder.interest_description = payload.interest_description

    await repo.flush()
    await db.commit()

    return stakeholder  # type: ignore


@router.delete(
    "/{stakeholder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def delete_stakeholder(
    project_id: uuid.UUID,
    stakeholder_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    repo: StakeholderRepository = Depends(get_repo),
) -> None:
    stakeholder = await repo.get(project_id=project_id, stakeholder_id=stakeholder_id)
    if stakeholder is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Stakeholder not found")
    await repo.delete(stakeholder)
    await db.commit()
