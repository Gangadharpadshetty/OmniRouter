from fastapi import APIRouter, Depends, HTTPException
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, PromptCreate, PromptUpdate, PromptResponse
from app.services.project_service import ProjectService, PromptService
from app.utils.dependencies import get_current_user, get_project_service, get_prompt_service

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse)
async def create_project(
    req: ProjectCreate,
    current_user: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    project = await service.create_project(current_user, req.name, req.description)
    return ProjectResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        created_at=project.created_at,
        updated_at=project.updated_at
    )

@router.get("", response_model=list[ProjectResponse])
async def list_projects(
    current_user: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    projects = await service.list_projects(current_user)
    return [
        ProjectResponse(
            id=p.id,
            user_id=p.user_id,
            name=p.name,
            description=p.description,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in projects
    ]

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    project = await service.get_project(project_id, current_user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        created_at=project.created_at,
        updated_at=project.updated_at
    )

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    req: ProjectUpdate,
    current_user: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    project = await service.update_project(project_id, current_user, req.name, req.description)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        created_at=project.created_at,
        updated_at=project.updated_at
    )

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: str = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service)
):
    success = await service.delete_project(project_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

@router.post("/{project_id}/prompts", response_model=PromptResponse)
async def create_prompt(
    project_id: str,
    req: PromptCreate,
    current_user: str = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    prompt_service: PromptService = Depends(get_prompt_service)
):
    # Verify project exists and belongs to user
    project = await project_service.get_project(project_id, current_user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    prompt = await prompt_service.create_prompt(project_id, req.name, req.content)
    return PromptResponse(
        id=prompt.id,
        project_id=prompt.project_id,
        name=prompt.name,
        content=prompt.content,
        version=prompt.version,
        created_at=prompt.created_at,
        updated_at=prompt.updated_at
    )

@router.get("/{project_id}/prompts", response_model=list[PromptResponse])
async def list_prompts(
    project_id: str,
    current_user: str = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    prompt_service: PromptService = Depends(get_prompt_service)
):
    # Verify project exists and belongs to user
    project = await project_service.get_project(project_id, current_user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    prompts = await prompt_service.list_prompts(project_id)
    return [
        PromptResponse(
            id=p.id,
            project_id=p.project_id,
            name=p.name,
            content=p.content,
            version=p.version,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in prompts
    ]

@router.put("/{project_id}/prompts/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    project_id: str,
    prompt_id: str,
    req: PromptUpdate,
    current_user: str = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    prompt_service: PromptService = Depends(get_prompt_service)
):
    # Verify project exists and belongs to user
    project = await project_service.get_project(project_id, current_user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    prompt = await prompt_service.update_prompt(prompt_id, req.name, req.content)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    return PromptResponse(
        id=prompt.id,
        project_id=prompt.project_id,
        name=prompt.name,
        content=prompt.content,
        version=prompt.version,
        created_at=prompt.created_at,
        updated_at=prompt.updated_at
    )

@router.delete("/{project_id}/prompts/{prompt_id}")
async def delete_prompt(
    project_id: str,
    prompt_id: str,
    current_user: str = Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
    prompt_service: PromptService = Depends(get_prompt_service)
):
    # Verify project exists and belongs to user
    project = await project_service.get_project(project_id, current_user)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    success = await prompt_service.delete_prompt(prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    return {"message": "Prompt deleted successfully"}
