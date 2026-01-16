import uuid
from datetime import datetime
from typing import List
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.project import Project, Prompt

Base = declarative_base()

class ProjectTable(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PromptTable(Base):
    __tablename__ = "prompts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    content = Column(String(10000), nullable=False)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PostgresProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: str, name: str, description: str | None) -> Project:
        project = ProjectTable(
            user_id=uuid.UUID(user_id),
            name=name,
            description=description
        )
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return Project(
            id=str(project.id),
            user_id=str(project.user_id),
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at
        )
    
    async def get_by_id(self, project_id: str, user_id: str) -> Project | None:
        result = await self.db.execute(
            select(ProjectTable).where(
                (ProjectTable.id == uuid.UUID(project_id)) & 
                (ProjectTable.user_id == uuid.UUID(user_id))
            )
        )
        row = result.scalar_one_or_none()
        if not row:
            return None
        return Project(
            id=str(row.id),
            user_id=str(row.user_id),
            name=row.name,
            description=row.description,
            created_at=row.created_at,
            updated_at=row.updated_at
        )
    
    async def list_by_user(self, user_id: str) -> List[Project]:
        result = await self.db.execute(
            select(ProjectTable).where(ProjectTable.user_id == uuid.UUID(user_id))
        )
        rows = result.scalars().all()
        return [
            Project(
                id=str(row.id),
                user_id=str(row.user_id),
                name=row.name,
                description=row.description,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            for row in rows
        ]
    
    async def update(self, project_id: str, user_id: str, name: str, description: str | None) -> Project | None:
        project = await self.get_by_id(project_id, user_id)
        if not project:
            return None
        
        result = await self.db.execute(
            select(ProjectTable).where(ProjectTable.id == uuid.UUID(project_id))
        )
        row = result.scalar_one_or_none()
        row.name = name
        row.description = description
        row.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(row)
        
        return Project(
            id=str(row.id),
            user_id=str(row.user_id),
            name=row.name,
            description=row.description,
            created_at=row.created_at,
            updated_at=row.updated_at
        )
    
    async def delete(self, project_id: str, user_id: str) -> bool:
        project = await self.get_by_id(project_id, user_id)
        if not project:
            return False
        
        result = await self.db.execute(
            select(ProjectTable).where(ProjectTable.id == uuid.UUID(project_id))
        )
        row = result.scalar_one_or_none()
        await self.db.delete(row)
        await self.db.commit()
        return True

class PostgresPromptRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, project_id: str, name: str, content: str) -> Prompt:
        prompt = PromptTable(
            project_id=uuid.UUID(project_id),
            name=name,
            content=content
        )
        self.db.add(prompt)
        await self.db.commit()
        await self.db.refresh(prompt)
        return Prompt(
            id=str(prompt.id),
            project_id=str(prompt.project_id),
            name=prompt.name,
            content=prompt.content,
            version=prompt.version,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at
        )
    
    async def get_by_id(self, prompt_id: str) -> Prompt | None:
        result = await self.db.execute(
            select(PromptTable).where(PromptTable.id == uuid.UUID(prompt_id))
        )
        row = result.scalar_one_or_none()
        if not row:
            return None
        return Prompt(
            id=str(row.id),
            project_id=str(row.project_id),
            name=row.name,
            content=row.content,
            version=row.version,
            created_at=row.created_at,
            updated_at=row.updated_at
        )
    
    async def list_by_project(self, project_id: str) -> List[Prompt]:
        result = await self.db.execute(
            select(PromptTable).where(PromptTable.project_id == uuid.UUID(project_id))
        )
        rows = result.scalars().all()
        return [
            Prompt(
                id=str(row.id),
                project_id=str(row.project_id),
                name=row.name,
                content=row.content,
                version=row.version,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            for row in rows
        ]
    
    async def update(self, prompt_id: str, name: str, content: str) -> Prompt | None:
        result = await self.db.execute(
            select(PromptTable).where(PromptTable.id == uuid.UUID(prompt_id))
        )
        row = result.scalar_one_or_none()
        if not row:
            return None
        
        row.name = name
        row.content = content
        row.version += 1
        row.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(row)
        
        return Prompt(
            id=str(row.id),
            project_id=str(row.project_id),
            name=row.name,
            content=row.content,
            version=row.version,
            created_at=row.created_at,
            updated_at=row.updated_at
        )
    
    async def delete(self, prompt_id: str) -> bool:
        result = await self.db.execute(
            select(PromptTable).where(PromptTable.id == uuid.UUID(prompt_id))
        )
        row = result.scalar_one_or_none()
        if not row:
            return False
        
        await self.db.delete(row)
        await self.db.commit()
        return True
