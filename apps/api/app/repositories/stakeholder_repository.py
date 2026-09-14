import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import StakeholderCategory
from app.models.stakeholder import Stakeholder


class StakeholderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_project(self, project_id: uuid.UUID) -> list[Stakeholder]:
        stmt = (
            select(Stakeholder)
            .where(Stakeholder.project_id == project_id)
            .order_by(Stakeholder.created_at)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, *, project_id: uuid.UUID, stakeholder_id: uuid.UUID) -> Stakeholder | None:
        stmt = select(Stakeholder).where(
            Stakeholder.id == stakeholder_id, Stakeholder.project_id == project_id
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        project_id: uuid.UUID,
        name: str,
        category: StakeholderCategory,
        interest_description: str | None,
    ) -> Stakeholder:
        stakeholder = Stakeholder(
            project_id=project_id,
            name=name,
            category=category,
            interest_description=interest_description,
        )
        self._session.add(stakeholder)
        await self._session.flush()
        return stakeholder

    async def delete(self, stakeholder: Stakeholder) -> None:
        await self._session.delete(stakeholder)
        await self._session.flush()

    async def flush(self) -> None:
        await self._session.flush()
