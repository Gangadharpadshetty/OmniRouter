from dataclasses import dataclass
from datetime import datetime
from typing import Literal

@dataclass
class Conversation:
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Message:
    id: str
    conversation_id: str
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime
