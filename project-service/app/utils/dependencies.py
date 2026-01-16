from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import os
from app.core.database import get_db
from app.repositories.postgres_project_repo import PostgresProjectRepository, PostgresPromptRepository
from app.services.project_service import ProjectService, PromptService

# Auth service URL from environment
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "https://omnirouter-auth1.onrender.com")

async def get_current_user(authorization: str = Header(None)) -> str:
    """Validate token by calling auth service."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # Call auth service to validate token
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/auth/validate",
                headers={"Authorization": authorization}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["user_id"]
            else:
                raise HTTPException(status_code=401, detail="Invalid token")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Auth service unavailable")
    except Exception:
        raise HTTPException(status_code=401, detail="Token validation failed")

def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    project_repo = PostgresProjectRepository(db)
    prompt_repo = PostgresPromptRepository(db)
    return ProjectService(project_repo, prompt_repo)

def get_prompt_service(db: AsyncSession = Depends(get_db)) -> PromptService:
    prompt_repo = PostgresPromptRepository(db)
    return PromptService(prompt_repo)
