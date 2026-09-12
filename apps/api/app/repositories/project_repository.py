import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project, ProjectMember, ProjectRole


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, *, name: str, description: str | None, owner_id: uuid.UUID) -> Project:
        project = Project(name=name, description=description, owner_id=owner_id)
        self._session.add(project)
        await self._session.flush()

        membership = ProjectMember(project_id=project.id, user_id=owner_id, role=ProjectRole.OWNER)
        self._session.add(membership)
        await self._session.flush()

        return project

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

    async def archive(self, project: Project) -> None:
        project.archived_at = datetime.now(UTC)
        await self._session.flush()

    async def flush(self) -> None:
        await self._session.flush()
