from typing import List
from app.domain.project import Project, Prompt
from app.repositories.project_repository import ProjectRepository, PromptRepository

class ProjectService:
    def __init__(self, project_repo: ProjectRepository, prompt_repo: PromptRepository):
        self.project_repo = project_repo
        self.prompt_repo = prompt_repo
    
    async def create_project(self, user_id: str, name: str, description: str | None) -> Project:
        return await self.project_repo.create(user_id, name, description)
    
    async def get_project(self, project_id: str, user_id: str) -> Project | None:
        return await self.project_repo.get_by_id(project_id, user_id)
    
    async def list_projects(self, user_id: str) -> List[Project]:
        return await self.project_repo.list_by_user(user_id)
    
    async def update_project(self, project_id: str, user_id: str, name: str, description: str | None) -> Project | None:
        return await self.project_repo.update(project_id, user_id, name, description)
    
    async def delete_project(self, project_id: str, user_id: str) -> bool:
        return await self.project_repo.delete(project_id, user_id)

class PromptService:
    def __init__(self, prompt_repo: PromptRepository):
        self.prompt_repo = prompt_repo
    
    async def create_prompt(self, project_id: str, name: str, content: str) -> Prompt:
        return await self.prompt_repo.create(project_id, name, content)
    
    async def get_prompt(self, prompt_id: str) -> Prompt | None:
        return await self.prompt_repo.get_by_id(prompt_id)
    
    async def list_prompts(self, project_id: str) -> List[Prompt]:
        return await self.prompt_repo.list_by_project(project_id)
    
    async def update_prompt(self, prompt_id: str, name: str, content: str) -> Prompt | None:
        return await self.prompt_repo.update(prompt_id, name, content)
    
    async def delete_prompt(self, prompt_id: str) -> bool:
        return await self.prompt_repo.delete(prompt_id)
