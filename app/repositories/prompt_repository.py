from typing import Protocol
from app.domain.prompt import Prompt

class PromptRepository(Protocol):
    async def create(
        self, project_id: str, role: str, content: str
    ) -> Prompt: ...

    async def list_by_project(self, project_id: str) -> list[Prompt]: ...
