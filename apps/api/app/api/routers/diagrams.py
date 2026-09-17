import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_project_role
from app.db.session import get_db
from app.models.project import ProjectRole
from app.repositories.diagram_repository import DiagramRepository
from app.schemas.diagram import DiagramCreate, DiagramRead, DiagramUpdate
from app.services.diagram_service import DiagramService

router = APIRouter(prefix="/projects/{project_id}/diagrams", tags=["diagrams"])


def get_service(db: AsyncSession = Depends(get_db)) -> DiagramService:
    return DiagramService(DiagramRepository(db))


@router.get(
    "",
    response_model=list[DiagramRead],
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def list_diagrams(
    project_id: uuid.UUID, service: DiagramService = Depends(get_service)
) -> list[DiagramRead]:
    return await service.list_diagrams(project_id)  # type: ignore


@router.post(
    "",
    response_model=DiagramRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def create_diagram(
    project_id: uuid.UUID,
    payload: DiagramCreate,
    db: AsyncSession = Depends(get_db),
    service: DiagramService = Depends(get_service),
) -> DiagramRead:
    diagram = await service.create_diagram(project_id=project_id, payload=payload)
    await db.commit()

    return diagram  # type: ignore


@router.get(
    "/{diagram_id}",
    response_model=DiagramRead,
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def get_diagram(
    project_id: uuid.UUID,
    diagram_id: uuid.UUID,
    service: DiagramService = Depends(get_service),
) -> DiagramRead:
    diagram = await service.get_diagram(project_id=project_id, diagram_id=diagram_id)
    if diagram is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Diagram not found")

    return diagram  # type: ignore


@router.patch(
    "/{diagram_id}",
    response_model=DiagramRead,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def update_diagram(
    project_id: uuid.UUID,
    diagram_id: uuid.UUID,
    payload: DiagramUpdate,
    db: AsyncSession = Depends(get_db),
    service: DiagramService = Depends(get_service),
) -> DiagramRead:
    diagram = await service.update_diagram(
        project_id=project_id, diagram_id=diagram_id, payload=payload
    )
    if diagram is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Diagram not found")

    await db.commit()
    await db.refresh(diagram)

    return diagram  # type: ignore


@router.delete(
    "/{diagram_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def delete_diagram(
    project_id: uuid.UUID,
    diagram_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    service: DiagramService = Depends(get_service),
) -> None:
    deleted = await service.delete_diagram(project_id=project_id, diagram_id=diagram_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Diagram not found")
    await db.commit()
