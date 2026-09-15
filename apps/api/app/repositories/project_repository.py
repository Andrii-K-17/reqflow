import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project, ProjectMember, ProjectRole


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, project: Project) -> None:
        self._session.add(project)

    def add_member(self, membership: ProjectMember) -> None:
        self._session.add(membership)

    async def get_by_id(self, project_id: uuid.UUID) -> Project | None:
        return await self._session.get(Project, project_id)

    async def list_for_user(self, user_id: uuid.UUID) -> list[tuple[Project, ProjectRole]]:
        stmt = (
            select(Project, ProjectMember.role)
            .join(ProjectMember, ProjectMember.project_id == Project.id)
            .where(ProjectMember.user_id == user_id, Project.archived_at.is_(None))
            .order_by(Project.created_at.desc())
        )
        result = await self._session.execute(stmt)

        return [(row[0], row[1]) for row in result.all()]

    async def get_membership(
        self,
        *,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> ProjectMember | None:
        stmt = select(ProjectMember).where(
            ProjectMember.project_id == project_id, ProjectMember.user_id == user_id
        )
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def flush(self) -> None:
        await self._session.flush()
