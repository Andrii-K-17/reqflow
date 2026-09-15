import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_story import UserStory


class UserStoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_for_project(self, project_id: uuid.UUID) -> list[UserStory]:
        stmt = (
            select(UserStory)
            .where(UserStory.project_id == project_id)
            .order_by(UserStory.created_at)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, *, project_id: uuid.UUID, user_story_id: uuid.UUID) -> UserStory | None:
        stmt = select(UserStory).where(
            UserStory.id == user_story_id, UserStory.project_id == project_id
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def count(self, project_id: uuid.UUID) -> int:
        stmt = select(func.count()).select_from(UserStory).where(UserStory.project_id == project_id)
        return (await self._session.execute(stmt)).scalar_one()

    def add(self, user_story: UserStory) -> None:
        self._session.add(user_story)

    async def delete(self, user_story: UserStory) -> None:
        await self._session.delete(user_story)

    async def flush(self) -> None:
        await self._session.flush()
