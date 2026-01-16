import uuid
from datetime import datetime
from typing import List
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.chat import Conversation, Message

Base = declarative_base()

class ConversationTable(Base):
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MessageTable(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # user or assistant
    content = Column(String(10000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PostgresConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, project_id: str) -> Conversation:
        conversation = ConversationTable(project_id=uuid.UUID(project_id))
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return Conversation(
            id=str(conversation.id),
            project_id=str(conversation.project_id),
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )
    
    async def get_by_id(self, conversation_id: str) -> Conversation | None:
        result = await self.db.execute(
            select(ConversationTable).where(ConversationTable.id == uuid.UUID(conversation_id))
        )
        row = result.scalar_one_or_none()
        if not row:
            return None
        return Conversation(
            id=str(row.id),
            project_id=str(row.project_id),
            created_at=row.created_at,
            updated_at=row.updated_at
        )
    
    async def list_by_project(self, project_id: str) -> List[Conversation]:
        result = await self.db.execute(
            select(ConversationTable).where(ConversationTable.project_id == uuid.UUID(project_id))
        )
        rows = result.scalars().all()
        return [
            Conversation(
                id=str(row.id),
                project_id=str(row.project_id),
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            for row in rows
        ]
    
    async def delete(self, conversation_id: str) -> bool:
        result = await self.db.execute(
            select(ConversationTable).where(ConversationTable.id == uuid.UUID(conversation_id))
        )
        row = result.scalar_one_or_none()
        if not row:
            return False
        
        await self.db.delete(row)
        await self.db.commit()
        return True

class PostgresMessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, conversation_id: str, role: str, content: str) -> Message:
        message = MessageTable(
            conversation_id=uuid.UUID(conversation_id),
            role=role,
            content=content
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return Message(
            id=str(message.id),
            conversation_id=str(message.conversation_id),
            role=message.role,
            content=message.content,
            created_at=message.created_at
        )
    
    async def get_by_id(self, message_id: str) -> Message | None:
        result = await self.db.execute(
            select(MessageTable).where(MessageTable.id == uuid.UUID(message_id))
        )
        row = result.scalar_one_or_none()
        if not row:
            return None
        return Message(
            id=str(row.id),
            conversation_id=str(row.conversation_id),
            role=row.role,
            content=row.content,
            created_at=row.created_at
        )
    
    async def list_by_conversation(self, conversation_id: str) -> List[Message]:
        result = await self.db.execute(
            select(MessageTable)
            .where(MessageTable.conversation_id == uuid.UUID(conversation_id))
            .order_by(MessageTable.created_at)
        )
        rows = result.scalars().all()
        return [
            Message(
                id=str(row.id),
                conversation_id=str(row.conversation_id),
                role=row.role,
                content=row.content,
                created_at=row.created_at
            )
            for row in rows
        ]
    
    async def delete(self, message_id: str) -> bool:
        result = await self.db.execute(
            select(MessageTable).where(MessageTable.id == uuid.UUID(message_id))
        )
        row = result.scalar_one_or_none()
        if not row:
            return False
        
        await self.db.delete(row)
        await self.db.commit()
        return True
