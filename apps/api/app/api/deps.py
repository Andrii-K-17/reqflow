import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import InvalidTokenError, decode_token
from app.db.session import get_db
from app.models.project import ProjectRole
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

_ROLE_RANK: dict[ProjectRole, int] = {
    ProjectRole.VIEWER: 0,
    ProjectRole.EDITOR: 1,
    ProjectRole.OWNER: 2,
}


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_project_repository(db: AsyncSession = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(db)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    users: UserRepository = Depends(get_user_repository),
) -> User:
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
    try:
        user_id: uuid.UUID = decode_token(token, "access")
    except InvalidTokenError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token") from exc

    user = await users.get_by_id(user_id)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User no longer exists")
    return user


def require_project_role(min_role: ProjectRole):
    """Ensure the user has at least `min_role` in the project and return their role."""

    async def dependency(
        project_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        projects: ProjectRepository = Depends(get_project_repository),
    ) -> ProjectRole:
        project = await projects.get_by_id(project_id)
        if project is None or project.archived_at is not None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

        membership = await projects.get_membership(project_id=project_id, user_id=current_user.id)
        if membership is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "You are not a member of this project")

        if _ROLE_RANK[membership.role] < _ROLE_RANK[min_role]:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient permissions")

        return membership.role

    return dependency
