import uuid

from sqlalchemy.exc import IntegrityError

from app.models.use_case import UseCase
from app.repositories.use_case_repository import UseCaseRepository
from app.schemas.use_case import UseCaseCreate, UseCaseUpdate

_MAX_CODE_GENERATION_ATTEMPTS = 5


class UseCaseService:
    def __init__(self, use_cases: UseCaseRepository) -> None:
        self._use_cases = use_cases

    async def create_use_case(self, *, project_id: uuid.UUID, payload: UseCaseCreate) -> UseCase:
        last_error: IntegrityError | None = None

        for _ in range(_MAX_CODE_GENERATION_ATTEMPTS):
            existing_count = await self._use_cases.count(project_id)
            code = f"UC-{existing_count + 1:03d}"
            use_case = UseCase(
                project_id=project_id,
                code=code,
                title=payload.title,
                actors=payload.actors,
                preconditions=payload.preconditions,
                postconditions=payload.postconditions,
                main_flow=payload.main_flow,
                alternative_flows=[flow.model_dump() for flow in payload.alternative_flows],
            )
            self._use_cases.add(use_case)
            try:
                await self._use_cases.flush()
                return use_case
            except IntegrityError as exc:
                last_error = exc
                continue

        assert last_error is not None
        raise last_error

    async def list_use_cases(self, project_id: uuid.UUID) -> list[UseCase]:
        return await self._use_cases.list_for_project(project_id)

    async def get_use_case(
        self, *, project_id: uuid.UUID, use_case_id: uuid.UUID
    ) -> UseCase | None:
        return await self._use_cases.get(project_id=project_id, use_case_id=use_case_id)

    async def update_use_case(
        self, *, project_id: uuid.UUID, use_case_id: uuid.UUID, payload: UseCaseUpdate
    ) -> UseCase | None:
        use_case = await self._use_cases.get(project_id=project_id, use_case_id=use_case_id)
        if use_case is None:
            return None

        if payload.title is not None:
            use_case.title = payload.title
        if payload.actors is not None:
            use_case.actors = payload.actors
        if payload.preconditions is not None:
            use_case.preconditions = payload.preconditions
        if payload.postconditions is not None:
            use_case.postconditions = payload.postconditions
        if payload.main_flow is not None:
            use_case.main_flow = payload.main_flow
        if payload.alternative_flows is not None:
            use_case.alternative_flows = [flow.model_dump() for flow in payload.alternative_flows]

        await self._use_cases.flush()
        return use_case

    async def delete_use_case(self, *, project_id: uuid.UUID, use_case_id: uuid.UUID) -> bool:
        use_case = await self._use_cases.get(project_id=project_id, use_case_id=use_case_id)
        if use_case is None:
            return False
        await self._use_cases.delete(use_case)
        await self._use_cases.flush()
        return True
