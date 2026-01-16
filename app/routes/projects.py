from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.project import ProjectCreate
from app.schemas.prompt import PromptCreate
from app.core.database import get_db
from app.utils.dependencies import get_current_user
from app.repositories.postgres_repo import (
    PostgresProjectRepository,
    PostgresPromptRepository
)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/")
async def create_project(
    payload: ProjectCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ProjectService(
        PostgresProjectRepository(db),
        PostgresPromptRepository(db)
    )
    return await service.create_project(user["user_id"], payload.name, payload.description)

@router.post("/{project_id}/prompts")
async def add_prompt(
    project_id: str,
    payload: PromptCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ProjectService(
        PostgresProjectRepository(db),
        PostgresPromptRepository(db)
    )
    return await service.add_prompt(
        project_id, user["user_id"], payload.role, payload.content
    )
