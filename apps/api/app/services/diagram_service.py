import uuid

from sqlalchemy.exc import IntegrityError

from app.models.diagram import Diagram
from app.repositories.diagram_repository import DiagramRepository
from app.schemas.diagram import DiagramCreate, DiagramUpdate

_MAX_CODE_GENERATION_ATTEMPTS = 5


class DiagramService:
    def __init__(self, diagrams: DiagramRepository) -> None:
        self._diagrams = diagrams

    async def create_diagram(self, *, project_id: uuid.UUID, payload: DiagramCreate) -> Diagram:
        last_error: IntegrityError | None = None

        for _ in range(_MAX_CODE_GENERATION_ATTEMPTS):
            existing_count = await self._diagrams.count(project_id)
            code = f"DG-{existing_count + 1:03d}"
            diagram = Diagram(
                project_id=project_id,
                code=code,
                title=payload.title,
                type=payload.type,
                mermaid_source=payload.mermaid_source,
            )
            self._diagrams.add(diagram)
            try:
                await self._diagrams.flush()
                return diagram
            except IntegrityError as exc:
                last_error = exc
                continue

        assert last_error is not None
        raise last_error

    async def list_diagrams(self, project_id: uuid.UUID) -> list[Diagram]:
        return await self._diagrams.list_for_project(project_id)

    async def get_diagram(self, *, project_id: uuid.UUID, diagram_id: uuid.UUID) -> Diagram | None:
        return await self._diagrams.get(project_id=project_id, diagram_id=diagram_id)

    async def update_diagram(
        self, *, project_id: uuid.UUID, diagram_id: uuid.UUID, payload: DiagramUpdate
    ) -> Diagram | None:
        diagram = await self._diagrams.get(project_id=project_id, diagram_id=diagram_id)
        if diagram is None:
            return None

        if payload.title is not None:
            diagram.title = payload.title
        if payload.mermaid_source is not None:
            diagram.mermaid_source = payload.mermaid_source

        await self._diagrams.flush()
        return diagram

    async def delete_diagram(self, *, project_id: uuid.UUID, diagram_id: uuid.UUID) -> bool:
        diagram = await self._diagrams.get(project_id=project_id, diagram_id=diagram_id)
        if diagram is None:
            return False

        await self._diagrams.delete(diagram)
        await self._diagrams.flush()

        return True
