from typing import List
from app.domain.chat import Conversation, Message
from app.repositories.chat_repository import ConversationRepository, MessageRepository
from app.services.llm_provider import LLMProvider, LLMMessage

class ConversationService:
    def __init__(self, conversation_repo: ConversationRepository):
        self.conversation_repo = conversation_repo
    
    async def create_conversation(self, project_id: str) -> Conversation:
        return await self.conversation_repo.create(project_id)
    
    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        return await self.conversation_repo.get_by_id(conversation_id)
    
    async def list_conversations(self, project_id: str) -> List[Conversation]:
        return await self.conversation_repo.list_by_project(project_id)
    
    async def delete_conversation(self, conversation_id: str) -> bool:
        return await self.conversation_repo.delete(conversation_id)

class MessageService:
    def __init__(self, message_repo: MessageRepository, llm_provider: LLMProvider):
        self.message_repo = message_repo
        self.llm_provider = llm_provider
    
    async def add_message(self, conversation_id: str, role: str, content: str) -> Message:
        return await self.message_repo.create(conversation_id, role, content)
    
    async def get_message(self, message_id: str) -> Message | None:
        return await self.message_repo.get_by_id(message_id)
    
    async def list_messages(self, conversation_id: str) -> List[Message]:
        return await self.message_repo.list_by_conversation(conversation_id)
    
    async def send_message_and_get_response(
        self, 
        conversation_id: str, 
        user_message: str
    ) -> str:
        """Add user message and get LLM response"""
        # Add user message
        await self.add_message(conversation_id, "user", user_message)
        
        # Get conversation history
        messages = await self.list_messages(conversation_id)
        
        # Prepare messages for LLM
        llm_messages = [
            LLMMessage(msg.role, msg.content) for msg in messages
        ]
        
        # Get LLM response
        response = await self.llm_provider.send_message(llm_messages)
        
        # Save assistant response
        await self.add_message(conversation_id, "assistant", response)
        
        return response
