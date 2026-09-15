import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_project_role
from app.db.session import get_db
from app.models.project import ProjectRole
from app.repositories.use_case_repository import UseCaseRepository
from app.schemas.use_case import UseCaseCreate, UseCaseRead, UseCaseUpdate
from app.services.use_case_service import UseCaseService

router = APIRouter(prefix="/projects/{project_id}/use-cases", tags=["use-cases"])


def get_service(db: AsyncSession = Depends(get_db)) -> UseCaseService:
    return UseCaseService(UseCaseRepository(db))


@router.get(
    "",
    response_model=list[UseCaseRead],
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def list_use_cases(
    project_id: uuid.UUID, service: UseCaseService = Depends(get_service)
) -> list[UseCaseRead]:
    return await service.list_use_cases(project_id)  # type: ignore


@router.post(
    "",
    response_model=UseCaseRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def create_use_case(
    project_id: uuid.UUID,
    payload: UseCaseCreate,
    db: AsyncSession = Depends(get_db),
    service: UseCaseService = Depends(get_service),
) -> UseCaseRead:
    use_case = await service.create_use_case(project_id=project_id, payload=payload)
    await db.commit()

    return use_case  # type: ignore


@router.get(
    "/{use_case_id}",
    response_model=UseCaseRead,
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def get_use_case(
    project_id: uuid.UUID,
    use_case_id: uuid.UUID,
    service: UseCaseService = Depends(get_service),
) -> UseCaseRead:
    use_case = await service.get_use_case(project_id=project_id, use_case_id=use_case_id)
    if use_case is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Use case not found")

    return use_case  # type: ignore


@router.patch(
    "/{use_case_id}",
    response_model=UseCaseRead,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def update_use_case(
    project_id: uuid.UUID,
    use_case_id: uuid.UUID,
    payload: UseCaseUpdate,
    db: AsyncSession = Depends(get_db),
    service: UseCaseService = Depends(get_service),
) -> UseCaseRead:
    use_case = await service.update_use_case(
        project_id=project_id, use_case_id=use_case_id, payload=payload
    )
    if use_case is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Use case not found")

    await db.commit()
    await db.refresh(use_case)

    return use_case  # type: ignore


@router.delete(
    "/{use_case_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def delete_use_case(
    project_id: uuid.UUID,
    use_case_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    service: UseCaseService = Depends(get_service),
) -> None:
    deleted = await service.delete_use_case(project_id=project_id, use_case_id=use_case_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Use case not found")

    await db.commit()
