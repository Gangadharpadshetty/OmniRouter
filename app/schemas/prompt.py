from pydantic import BaseModel

class PromptCreate(BaseModel):
    role: str
    content: str
