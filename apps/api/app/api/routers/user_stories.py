import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_project_role
from app.db.session import get_db
from app.models.project import ProjectRole
from app.repositories.user_story_repository import UserStoryRepository
from app.schemas.user_story import UserStoryCreate, UserStoryRead, UserStoryUpdate
from app.services.user_story_service import UserStoryService

router = APIRouter(prefix="/projects/{project_id}/user-stories", tags=["user-stories"])


def get_service(db: AsyncSession = Depends(get_db)) -> UserStoryService:
    return UserStoryService(UserStoryRepository(db))


@router.get(
    "",
    response_model=list[UserStoryRead],
    dependencies=[Depends(require_project_role(ProjectRole.VIEWER))],
)
async def list_user_stories(
    project_id: uuid.UUID, service: UserStoryService = Depends(get_service)
) -> list[UserStoryRead]:
    return await service.list_user_stories(project_id)  # type: ignore


@router.post(
    "",
    response_model=UserStoryRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def create_user_story(
    project_id: uuid.UUID,
    payload: UserStoryCreate,
    db: AsyncSession = Depends(get_db),
    service: UserStoryService = Depends(get_service),
) -> UserStoryRead:
    user_story = await service.create_user_story(project_id=project_id, payload=payload)

    await db.commit()

    return user_story  # type: ignore


@router.patch(
    "/{user_story_id}",
    response_model=UserStoryRead,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def update_user_story(
    project_id: uuid.UUID,
    user_story_id: uuid.UUID,
    payload: UserStoryUpdate,
    db: AsyncSession = Depends(get_db),
    service: UserStoryService = Depends(get_service),
) -> UserStoryRead:
    user_story = await service.update_user_story(
        project_id=project_id, user_story_id=user_story_id, payload=payload
    )
    if user_story is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User story not found")

    await db.commit()
    await db.refresh(user_story)

    return user_story  # type: ignore


@router.delete(
    "/{user_story_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_project_role(ProjectRole.EDITOR))],
)
async def delete_user_story(
    project_id: uuid.UUID,
    user_story_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    service: UserStoryService = Depends(get_service),
) -> None:
    deleted = await service.delete_user_story(project_id=project_id, user_story_id=user_story_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User story not found")

    await db.commit()
