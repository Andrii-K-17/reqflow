import uuid
from datetime import UTC, datetime

from app.models.project import Project, ProjectMember, ProjectRole
from app.repositories.project_repository import ProjectRepository

WRITE_ROLES = {ProjectRole.OWNER, ProjectRole.EDITOR}


class ProjectNotFoundError(Exception):
    pass


class ProjectAccessDeniedError(Exception):
    pass


class ProjectService:
    def __init__(self, projects: ProjectRepository) -> None:
        self._projects = projects

    async def create_project(
        self,
        *,
        name: str,
        description: str | None,
        owner_id: uuid.UUID,
    ) -> tuple[Project, ProjectRole]:
        project = Project(name=name, description=description, owner_id=owner_id)
        self._projects.add(project)
        await self._projects.flush()
        self._projects.add_member(
            ProjectMember(project_id=project.id, user_id=owner_id, role=ProjectRole.OWNER)
        )
        await self._projects.flush()
        return project, ProjectRole.OWNER

    async def list_projects(self, user_id: uuid.UUID) -> list[tuple[Project, ProjectRole]]:
        return await self._projects.list_for_user(user_id)

    async def get_project(
        self,
        *,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> tuple[Project, ProjectRole]:
        project = await self._projects.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError("Project not found")

        membership = await self._projects.get_membership(project_id=project_id, user_id=user_id)
        if membership is None:
            raise ProjectAccessDeniedError("You are not a member of this project")

        return project, membership.role

    async def update_project(
        self,
        *,
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        name: str | None,
        description: str | None,
    ) -> tuple[Project, ProjectRole]:
        project, role = await self.get_project(project_id=project_id, user_id=user_id)
        if role not in WRITE_ROLES:
            raise ProjectAccessDeniedError("Insufficient permissions to edit this project")

        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        await self._projects.flush()

        return project, role

    async def archive_project(self, *, project_id: uuid.UUID, user_id: uuid.UUID) -> None:
        project, role = await self.get_project(project_id=project_id, user_id=user_id)
        if role != ProjectRole.OWNER:
            raise ProjectAccessDeniedError("Only the owner can archive a project")
        project.archived_at = datetime.now(UTC)
        await self._projects.flush()
