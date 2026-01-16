from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class ConversationCreate(BaseModel):
    pass

class ConversationResponse(BaseModel):
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime

class SendMessageRequest(BaseModel):
    content: str

class SendMessageResponse(BaseModel):
    message_id: str
    response: str
    created_at: datetime
