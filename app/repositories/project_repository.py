from typing import Protocol
from app.domain.project import Project

class ProjectRepository(Protocol):
    async def create(
        self, user_id: str, name: str, description: str | None
    ) -> Project: ...

    async def list_by_user(self, user_id: str) -> list[Project]: ...

    async def get_by_id(self, project_id: str) -> Project | None: ...
