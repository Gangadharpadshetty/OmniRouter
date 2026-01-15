import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.user import User

Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MySQLUserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(UserTable).where(UserTable.email == email)
        )
        row = result.scalar_one_or_none()
        if not row:
            return None
        return User(
            id=str(row.id),
            email=row.email,
            password_hash=row.password_hash,
            created_at=row.created_at
        )

    async def create(self, email: str, password_hash: str) -> User:
        user = UserTable(email=email, password_hash=password_hash)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return User(
            id=str(user.id),
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at
        )
