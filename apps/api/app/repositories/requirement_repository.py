import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Priority, RequirementStatus, RequirementType
from app.models.requirement import Requirement


class RequirementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_project(
        self,
        *,
        project_id: uuid.UUID,
        req_type: RequirementType | None,
        status_filter: RequirementStatus | None,
        priority: Priority | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Requirement], int]:
        stmt = select(Requirement).where(Requirement.project_id == project_id)
        count_stmt = (
            select(func.count())
            .select_from(Requirement)
            .where(Requirement.project_id == project_id)
        )

        if req_type is not None:
            stmt = stmt.where(Requirement.type == req_type)
            count_stmt = count_stmt.where(Requirement.type == req_type)
        if status_filter is not None:
            stmt = stmt.where(Requirement.status == status_filter)
            count_stmt = count_stmt.where(Requirement.status == status_filter)
        if priority is not None:
            stmt = stmt.where(Requirement.priority == priority)
            count_stmt = count_stmt.where(Requirement.priority == priority)

        stmt = stmt.order_by(Requirement.created_at).offset((page - 1) * page_size).limit(page_size)

        total = (await self._session.execute(count_stmt)).scalar_one()
        items = list((await self._session.execute(stmt)).scalars().all())

        return items, total

    async def get(self, *, project_id: uuid.UUID, requirement_id: uuid.UUID) -> Requirement | None:
        stmt = select(Requirement).where(
            Requirement.id == requirement_id, Requirement.project_id == project_id
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def count_by_type(self, *, project_id: uuid.UUID, req_type: RequirementType) -> int:
        stmt = (
            select(func.count())
            .select_from(Requirement)
            .where(Requirement.project_id == project_id, Requirement.type == req_type)
        )
        return (await self._session.execute(stmt)).scalar_one()

    def add(self, requirement: Requirement) -> None:
        self._session.add(requirement)

    async def delete(self, requirement: Requirement) -> None:
        await self._session.delete(requirement)

    async def flush(self) -> None:
        await self._session.flush()
