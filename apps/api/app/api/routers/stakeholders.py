import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_project_role
from app.db.session import get_db
from app.models.project import ProjectRole
from app.repositories.stakeholder_repository import StakeholderRepository
from app.schemas.stakeholder import StakeholderCreate, StakeholderRead, StakeholderUpdate
from app.services.stakeholder_service import StakeholderService

router = APIRouter(prefix="/projects/{project_id}/stakeholders", tags=["stakeholders"])


def get_service(db: AsyncSession = Depends(get_db)) -> StakeholderService:
    return StakeholderService(StakeholderRepository(db))


@router.get(
    "",
    response_model=list[StakeholderRead],
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def list_stakeholders(
    project_id: uuid.UUID, service: StakeholderService = Depends(get_service)
) -> list[StakeholderRead]:
    return await service.list_stakeholders(project_id)  # type: ignore


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
    service: StakeholderService = Depends(get_service),
) -> StakeholderRead:
    stakeholder = await service.create_stakeholder(project_id=project_id, payload=payload)
    await db.commit()
    await db.refresh(stakeholder)
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
    service: StakeholderService = Depends(get_service),
) -> StakeholderRead:
    stakeholder = await service.update_stakeholder(
        project_id=project_id, stakeholder_id=stakeholder_id, payload=payload
    )
    if stakeholder is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Stakeholder not found")
    await db.commit()
    await db.refresh(stakeholder)

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
    service: StakeholderService = Depends(get_service),
) -> None:
    deleted = await service.delete_stakeholder(project_id=project_id, stakeholder_id=stakeholder_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Stakeholder not found")
    await db.commit()
