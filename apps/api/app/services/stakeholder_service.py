import uuid

from app.models.stakeholder import Stakeholder
from app.repositories.stakeholder_repository import StakeholderRepository
from app.schemas.stakeholder import StakeholderCreate, StakeholderUpdate


class StakeholderService:
    def __init__(self, stakeholders: StakeholderRepository) -> None:
        self._stakeholders = stakeholders

    async def list_stakeholders(self, project_id: uuid.UUID) -> list[Stakeholder]:
        return await self._stakeholders.list_for_project(project_id)

    async def create_stakeholder(
        self, *, project_id: uuid.UUID, payload: StakeholderCreate
    ) -> Stakeholder:
        stakeholder = Stakeholder(
            project_id=project_id,
            name=payload.name,
            category=payload.category,
            interest_description=payload.interest_description,
        )
        self._stakeholders.add(stakeholder)
        await self._stakeholders.flush()
        return stakeholder

    async def update_stakeholder(
        self, *, project_id: uuid.UUID, stakeholder_id: uuid.UUID, payload: StakeholderUpdate
    ) -> Stakeholder | None:
        stakeholder = await self._stakeholders.get(
            project_id=project_id, stakeholder_id=stakeholder_id
        )
        if stakeholder is None:
            return None

        if payload.name is not None:
            stakeholder.name = payload.name
        if payload.category is not None:
            stakeholder.category = payload.category
        if payload.interest_description is not None:
            stakeholder.interest_description = payload.interest_description

        await self._stakeholders.flush()
        return stakeholder

    async def delete_stakeholder(self, *, project_id: uuid.UUID, stakeholder_id: uuid.UUID) -> bool:
        stakeholder = await self._stakeholders.get(
            project_id=project_id, stakeholder_id=stakeholder_id
        )
        if stakeholder is None:
            return False
        await self._stakeholders.delete(stakeholder)
        await self._stakeholders.flush()
        return True
