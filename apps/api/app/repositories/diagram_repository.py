import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.diagram import Diagram


class DiagramRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_project(self, project_id: uuid.UUID) -> list[Diagram]:
        stmt = select(Diagram).where(Diagram.project_id == project_id).order_by(Diagram.created_at)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, *, project_id: uuid.UUID, diagram_id: uuid.UUID) -> Diagram | None:
        stmt = select(Diagram).where(Diagram.id == diagram_id, Diagram.project_id == project_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def count(self, project_id: uuid.UUID) -> int:
        stmt = select(func.count()).select_from(Diagram).where(Diagram.project_id == project_id)
        return (await self._session.execute(stmt)).scalar_one()

    def add(self, diagram: Diagram) -> None:
        self._session.add(diagram)

    async def delete(self, diagram: Diagram) -> None:
        await self._session.delete(diagram)

    async def flush(self) -> None:
        await self._session.flush()
