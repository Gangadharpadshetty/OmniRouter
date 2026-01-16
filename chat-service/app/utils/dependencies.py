from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import os
from app.core.database import get_db
from app.repositories.postgres_chat_repo import PostgresConversationRepository, PostgresMessageRepository
from app.services.chat_service import ConversationService, MessageService
from app.services.llm_provider import get_llm_provider

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

def get_conversation_service(db: AsyncSession = Depends(get_db)) -> ConversationService:
    conversation_repo = PostgresConversationRepository(db)
    return ConversationService(conversation_repo)

def get_message_service(db: AsyncSession = Depends(get_db)) -> MessageService:
    message_repo = PostgresMessageRepository(db)
    llm_provider = get_llm_provider()
    return MessageService(message_repo, llm_provider)
