import uuid

from sqlalchemy.exc import IntegrityError

from app.models.enums import (
    REQUIREMENT_CODE_PREFIX,
    Priority,
    RequirementStatus,
    RequirementType,
)
from app.models.requirement import Requirement
from app.repositories.requirement_repository import RequirementRepository
from app.schemas.requirement import RequirementCreate, RequirementUpdate


class RequirementService:
    def __init__(self, requirements: RequirementRepository) -> None:
        self._requirements = requirements

    async def _generate_code(self, *, project_id: uuid.UUID, req_type: RequirementType) -> str:
        prefix = REQUIREMENT_CODE_PREFIX[req_type]
        existing_count = await self._requirements.count_by_type(
            project_id=project_id, req_type=req_type
        )
        return f"{prefix}-{existing_count + 1:03d}"

    async def create_requirement(
        self, *, project_id: uuid.UUID, payload: RequirementCreate
    ) -> Requirement:
        """Create a new requirement with an auto-generated unique code.

        Attempts to generate and persist a requirement code with an optimistic
        retry mechanism to resolve concurrent creation collisions."""

        last_error: IntegrityError | None = None

        for _ in range(5):
            code = await self._generate_code(project_id=project_id, req_type=payload.type)
            requirement = Requirement(
                project_id=project_id,
                code=code,
                type=payload.type,
                title=payload.title,
                description=payload.description,
                priority=payload.priority,
                status=RequirementStatus.DRAFT,
                verifiable=payload.verifiable,
                rationale=payload.rationale,
                source=payload.source,
            )
            self._requirements.add(requirement)
            try:
                await self._requirements.flush()
                return requirement
            except IntegrityError as exc:
                last_error = exc
                continue

        assert last_error is not None
        raise last_error

    async def list_requirements(
        self,
        *,
        project_id: uuid.UUID,
        req_type: RequirementType | None,
        status_filter: RequirementStatus | None,
        priority: Priority | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Requirement], int]:
        return await self._requirements.list_for_project(
            project_id=project_id,
            req_type=req_type,
            status_filter=status_filter,
            priority=priority,
            page=page,
            page_size=page_size,
        )

    async def get_requirement(
        self, *, project_id: uuid.UUID, requirement_id: uuid.UUID
    ) -> Requirement | None:
        return await self._requirements.get(project_id=project_id, requirement_id=requirement_id)

    async def update_requirement(
        self, *, project_id: uuid.UUID, requirement_id: uuid.UUID, payload: RequirementUpdate
    ) -> Requirement | None:
        requirement = await self._requirements.get(
            project_id=project_id, requirement_id=requirement_id
        )
        if requirement is None:
            return None

        if payload.title is not None:
            requirement.title = payload.title
        if payload.description is not None:
            requirement.description = payload.description
        if payload.priority is not None:
            requirement.priority = payload.priority
        if payload.status is not None:
            requirement.status = payload.status
        if payload.verifiable is not None:
            requirement.verifiable = payload.verifiable
        if payload.rationale is not None:
            requirement.rationale = payload.rationale
        if payload.source is not None:
            requirement.source = payload.source

        await self._requirements.flush()

        return requirement

    async def delete_requirement(self, *, project_id: uuid.UUID, requirement_id: uuid.UUID) -> bool:
        requirement = await self._requirements.get(
            project_id=project_id, requirement_id=requirement_id
        )
        if requirement is None:
            return False

        await self._requirements.delete(requirement)
        await self._requirements.flush()

        return True
