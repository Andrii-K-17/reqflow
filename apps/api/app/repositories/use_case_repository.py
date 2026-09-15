import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.use_case import UseCase


class UseCaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_project(self, project_id: uuid.UUID) -> list[UseCase]:
        stmt = select(UseCase).where(UseCase.project_id == project_id).order_by(UseCase.created_at)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, *, project_id: uuid.UUID, use_case_id: uuid.UUID) -> UseCase | None:
        stmt = select(UseCase).where(UseCase.id == use_case_id, UseCase.project_id == project_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def count(self, project_id: uuid.UUID) -> int:
        stmt = select(func.count()).select_from(UseCase).where(UseCase.project_id == project_id)
        return (await self._session.execute(stmt)).scalar_one()

    def add(self, use_case: UseCase) -> None:
        self._session.add(use_case)

    async def delete(self, use_case: UseCase) -> None:
        await self._session.delete(use_case)

    async def flush(self) -> None:
        await self._session.flush()
