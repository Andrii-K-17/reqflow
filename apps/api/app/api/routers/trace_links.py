import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_project_role
from app.db.session import get_db
from app.models.project import ProjectRole
from app.repositories.trace_link_repository import TraceLinkRepository
from app.schemas.trace_link import TraceGraph, TraceLinkCreate, TraceLinkRead
from app.services.entity_resolver import EntityResolver
from app.services.traceability_service import (
    DuplicateTraceLinkError,
    EntityNotFoundError,
    TraceabilityService,
    TraceCycleError,
)

router = APIRouter(prefix="/projects/{project_id}/trace-links", tags=["traceability"])


def get_service(db: AsyncSession = Depends(get_db)) -> TraceabilityService:
    return TraceabilityService(TraceLinkRepository(db), EntityResolver(db))


@router.get(
    "",
    response_model=list[TraceLinkRead],
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def list_trace_links(
    project_id: uuid.UUID, service: TraceabilityService = Depends(get_service)
) -> list[TraceLinkRead]:
    return await service.list_links(project_id)  # type: ignore


@router.get(
    "/graph",
    response_model=TraceGraph,
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def get_trace_graph(
    project_id: uuid.UUID, service: TraceabilityService = Depends(get_service)
) -> TraceGraph:
    return await service.build_graph(project_id)


@router.post(
    "",
    response_model=TraceLinkRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def create_trace_link(
    project_id: uuid.UUID,
    payload: TraceLinkCreate,
    db: AsyncSession = Depends(get_db),
    service: TraceabilityService = Depends(get_service),
) -> TraceLinkRead:
    try:
        link = await service.create_link(project_id=project_id, payload=payload)
    except EntityNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except DuplicateTraceLinkError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except TraceCycleError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    await db.commit()
    return link  # type: ignore


@router.delete(
    "/{link_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def delete_trace_link(
    project_id: uuid.UUID,
    link_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    service: TraceabilityService = Depends(get_service),
) -> None:
    deleted = await service.delete_link(project_id=project_id, link_id=link_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trace link not found")
    await db.commit()
