from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_token
from app.repositories.postgres_chat_repo import PostgresConversationRepository, PostgresMessageRepository
from app.services.chat_service import ConversationService, MessageService
from app.services.llm_provider import get_llm_provider

async def get_current_user(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_id

def get_conversation_service(db: AsyncSession = Depends(get_db)) -> ConversationService:
    conversation_repo = PostgresConversationRepository(db)
    return ConversationService(conversation_repo)

def get_message_service(db: AsyncSession = Depends(get_db)) -> MessageService:
    message_repo = PostgresMessageRepository(db)
    llm_provider = get_llm_provider()
    return MessageService(message_repo, llm_provider)
