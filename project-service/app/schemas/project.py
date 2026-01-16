from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

class PromptCreate(BaseModel):
    name: str
    content: str

class PromptUpdate(BaseModel):
    name: str
    content: str

class PromptResponse(BaseModel):
    id: str
    project_id: str
    name: str
    content: str
    version: int
    created_at: datetime
    updated_at: datetime
