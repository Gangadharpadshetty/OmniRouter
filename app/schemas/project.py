from pydantic import BaseModel
from typing import Optional, List


class ProjectCreate(BaseModel):
	title: str
	description: Optional[str] = None


class ProjectOut(BaseModel):
	id: str
	owner_id: str
	title: str
	description: Optional[str] = None
	created_at: Optional[str] = None

	class Config:
		orm_mode = True


class PromptCreate(BaseModel):
	prompt_text: str


class PromptOut(BaseModel):
	id: str
	project_id: str
	prompt_text: str
	created_at: Optional[str] = None

	class Config:
		orm_mode = True
