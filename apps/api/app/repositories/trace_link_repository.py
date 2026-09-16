import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import TraceEntityType, TraceRelation
from app.models.trace_link import TraceLink


class TraceLinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_project(self, project_id: uuid.UUID) -> list[TraceLink]:
        stmt = (
            select(TraceLink)
            .where(TraceLink.project_id == project_id)
            .order_by(TraceLink.created_at)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, *, project_id: uuid.UUID, link_id: uuid.UUID) -> TraceLink | None:
        stmt = select(TraceLink).where(TraceLink.id == link_id, TraceLink.project_id == project_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists(
        self,
        *,
        project_id: uuid.UUID,
        from_type: TraceEntityType,
        from_id: uuid.UUID,
        to_type: TraceEntityType,
        to_id: uuid.UUID,
        relation: TraceRelation,
    ) -> bool:
        stmt = select(TraceLink).where(
            TraceLink.project_id == project_id,
            TraceLink.from_type == from_type,
            TraceLink.from_id == from_id,
            TraceLink.to_type == to_type,
            TraceLink.to_id == to_id,
            TraceLink.relation == relation,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def add(self, link: TraceLink) -> None:
        self._session.add(link)

    async def delete(self, link: TraceLink) -> None:
        await self._session.delete(link)

    async def flush(self) -> None:
        await self._session.flush()
