from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_token
from app.repositories.postgres_project_repo import PostgresProjectRepository, PostgresPromptRepository
from app.services.project_service import ProjectService, PromptService

async def get_current_user(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_id

def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    project_repo = PostgresProjectRepository(db)
    prompt_repo = PostgresPromptRepository(db)
    return ProjectService(project_repo, prompt_repo)

def get_prompt_service(db: AsyncSession = Depends(get_db)) -> PromptService:
    prompt_repo = PostgresPromptRepository(db)
    return PromptService(prompt_repo)
