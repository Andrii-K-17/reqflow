import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_project_role
from app.db.session import get_db
from app.models.enums import Priority, RequirementStatus, RequirementType
from app.models.project import ProjectRole
from app.repositories.requirement_repository import RequirementRepository
from app.schemas.requirement import (
    RequirementCreate,
    RequirementPage,
    RequirementRead,
    RequirementUpdate,
)
from app.services.requirement_service import RequirementService

router = APIRouter(prefix="/projects/{project_id}/requirements", tags=["requirements"])


def get_service(db: AsyncSession = Depends(get_db)) -> RequirementService:
    return RequirementService(RequirementRepository(db))


@router.get(
    "",
    response_model=RequirementPage,
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def list_requirements(
    project_id: uuid.UUID,
    type: RequirementType | None = Query(default=None),
    status: RequirementStatus | None = Query(default=None),
    priority: Priority | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: RequirementService = Depends(get_service),
) -> RequirementPage:
    items, total = await service.list_requirements(
        project_id=project_id,
        req_type=type,
        status_filter=status,
        priority=priority,
        page=page,
        page_size=page_size,
    )
    return RequirementPage(
        items=items,  # type: ignore
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post(
    "",
    response_model=RequirementRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def create_requirement(
    project_id: uuid.UUID,
    payload: RequirementCreate,
    db: AsyncSession = Depends(get_db),
    service: RequirementService = Depends(get_service),
) -> RequirementRead:
    requirement = await service.create_requirement(project_id=project_id, payload=payload)
    await db.commit()
    return requirement  # type: ignore


@router.get(
    "/{requirement_id}",
    response_model=RequirementRead,
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def get_requirement(
    project_id: uuid.UUID,
    requirement_id: uuid.UUID,
    service: RequirementService = Depends(get_service),
) -> RequirementRead:
    requirement = await service.get_requirement(
        project_id=project_id, requirement_id=requirement_id
    )
    if requirement is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Requirement not found")
    return requirement  # type: ignore


@router.patch(
    "/{requirement_id}",
    response_model=RequirementRead,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def update_requirement(
    project_id: uuid.UUID,
    requirement_id: uuid.UUID,
    payload: RequirementUpdate,
    db: AsyncSession = Depends(get_db),
    service: RequirementService = Depends(get_service),
) -> RequirementRead:
    requirement = await service.update_requirement(
        project_id=project_id, requirement_id=requirement_id, payload=payload
    )
    if requirement is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Requirement not found")
    await db.commit()
    return requirement  # type: ignore


@router.delete(
    "/{requirement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def delete_requirement(
    project_id: uuid.UUID,
    requirement_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    service: RequirementService = Depends(get_service),
) -> None:
    deleted = await service.delete_requirement(project_id=project_id, requirement_id=requirement_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Requirement not found")
    await db.commit()
