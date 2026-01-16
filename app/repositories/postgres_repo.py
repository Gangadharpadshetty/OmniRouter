import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.project import Project
from app.domain.prompt import Prompt

Base = declarative_base()

class ProjectTable(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class PromptTable(Base):
    __tablename__ = "prompts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    role = Column(String(50))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class PostgresProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: str, name: str, description: str | None):
        obj = ProjectTable(user_id=user_id, name=name, description=description)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return Project(str(obj.id), str(obj.user_id), obj.name, obj.description, obj.created_at)

    async def list_by_user(self, user_id: str):
        res = await self.db.execute(
            select(ProjectTable).where(ProjectTable.user_id == user_id)
        )
        return [
            Project(str(p.id), str(p.user_id), p.name, p.description, p.created_at)
            for p in res.scalars().all()
        ]

    async def get_by_id(self, project_id: str):
        res = await self.db.execute(
            select(ProjectTable).where(ProjectTable.id == project_id)
        )
        p = res.scalar_one_or_none()
        if not p:
            return None
        return Project(str(p.id), str(p.user_id), p.name, p.description, p.created_at)


class PostgresPromptRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, project_id: str, role: str, content: str):
        obj = PromptTable(project_id=project_id, role=role, content=content)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return Prompt(str(obj.id), str(obj.project_id), obj.role, obj.content, obj.created_at)

    async def list_by_project(self, project_id: str):
        res = await self.db.execute(
            select(PromptTable).where(PromptTable.project_id == project_id)
        )
        return [
            Prompt(str(p.id), str(p.project_id), p.role, p.content, p.created_at)
            for p in res.scalars().all()
        ]
