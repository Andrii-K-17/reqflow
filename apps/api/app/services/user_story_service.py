import uuid

from sqlalchemy.exc import IntegrityError

from app.models.user_story import UserStory
from app.repositories.user_story_repository import UserStoryRepository
from app.schemas.user_story import UserStoryCreate, UserStoryUpdate

_MAX_CODE_GENERATION_ATTEMPTS = 5


class UserStoryService:
    def __init__(self, user_stories: UserStoryRepository) -> None:
        self._user_stories = user_stories

    async def create_user_story(
        self, *, project_id: uuid.UUID, payload: UserStoryCreate
    ) -> UserStory:
        last_error: IntegrityError | None = None

        for _ in range(_MAX_CODE_GENERATION_ATTEMPTS):
            existing_count = await self._user_stories.count(project_id)
            code = f"US-{existing_count + 1:03d}"
            user_story = UserStory(
                project_id=project_id,
                code=code,
                role=payload.role,
                goal=payload.goal,
                benefit=payload.benefit,
                acceptance_criteria=payload.acceptance_criteria,
            )
            self._user_stories.add(user_story)
            try:
                await self._user_stories.flush()
                return user_story
            except IntegrityError as exc:
                last_error = exc
                continue

        assert last_error is not None
        raise last_error

    async def list_user_stories(self, project_id: uuid.UUID) -> list[UserStory]:
        return await self._user_stories.list_for_project(project_id)

    async def get_user_story(
        self, *, project_id: uuid.UUID, user_story_id: uuid.UUID
    ) -> UserStory | None:
        return await self._user_stories.get(project_id=project_id, user_story_id=user_story_id)

    async def update_user_story(
        self, *, project_id: uuid.UUID, user_story_id: uuid.UUID, payload: UserStoryUpdate
    ) -> UserStory | None:
        user_story = await self._user_stories.get(
            project_id=project_id, user_story_id=user_story_id
        )
        if user_story is None:
            return None

        if payload.role is not None:
            user_story.role = payload.role
        if payload.goal is not None:
            user_story.goal = payload.goal
        if payload.benefit is not None:
            user_story.benefit = payload.benefit
        if payload.acceptance_criteria is not None:
            user_story.acceptance_criteria = payload.acceptance_criteria

        await self._user_stories.flush()

        return user_story

    async def delete_user_story(self, *, project_id: uuid.UUID, user_story_id: uuid.UUID) -> bool:
        user_story = await self._user_stories.get(
            project_id=project_id, user_story_id=user_story_id
        )
        if user_story is None:
            return False

        await self._user_stories.delete(user_story)
        await self._user_stories.flush()

        return True
