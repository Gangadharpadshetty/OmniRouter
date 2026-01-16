from fastapi import HTTPException, status
from app.repositories.project_repository import ProjectRepository
from app.repositories.prompt_repository import PromptRepository

class ProjectService:
    def __init__(self, projects: ProjectRepository, prompts: PromptRepository):
        self.projects = projects
        self.prompts = prompts

    async def create_project(self, user_id: str, name: str, description: str | None):
        return await self.projects.create(user_id, name, description)

    async def list_projects(self, user_id: str):
        return await self.projects.list_by_user(user_id)

    async def add_prompt(self, project_id: str, user_id: str, role: str, content: str):
        project = await self.projects.get_by_id(project_id)
        if not project or project.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        return await self.prompts.create(project_id, role, content)
