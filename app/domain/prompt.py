from dataclasses import dataclass
from datetime import datetime

@dataclass
class Prompt:
    id: str
    project_id: str
    role: str
    content: str
    created_at: datetime
