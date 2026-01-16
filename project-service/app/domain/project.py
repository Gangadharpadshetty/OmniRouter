from dataclasses import dataclass
from datetime import datetime

@dataclass
class Project:
    id: str
    user_id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

@dataclass
class Prompt:
    id: str
    project_id: str
    name: str
    content: str
    version: int = 1
    created_at: datetime = None
    updated_at: datetime = None
