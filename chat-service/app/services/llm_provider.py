from abc import ABC, abstractmethod
from typing import List
import httpx
from app.core.config import settings

class LLMMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

class LLMProvider(ABC):
    @abstractmethod
    async def send_message(self, messages: List[LLMMessage]) -> str:
        """Send messages to LLM and return response"""
        pass

class OpenRouterProvider(LLMProvider):
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.LLM_MODEL
        self.base_url = "https://openrouter.ai/api/v1"
    
    async def send_message(self, messages: List[LLMMessage]) -> str:
        """Call OpenRouter API"""
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not configured")
        
        payload = {
            "model": self.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.LLM_MODEL
        self.base_url = "https://api.openai.com/v1"
    
    async def send_message(self, messages: List[LLMMessage]) -> str:
        """Call OpenAI API"""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        
        payload = {
            "model": self.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

def get_llm_provider() -> LLMProvider:
    """Factory function to get appropriate LLM provider"""
    if settings.LLM_PROVIDER == "openai":
        return OpenAIProvider()
    else:
        return OpenRouterProvider()
