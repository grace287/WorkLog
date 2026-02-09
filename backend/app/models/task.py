# backend/app/models/task.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """태스크 상태"""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskPriority(str, enum.Enum):
    """태스크 우선순위"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(Base):
    """태스크 모델"""
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)

    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    order = Column(Integer, default=0)  # 정렬 순서

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="tasks")

    def __repr__(self):
        return f"<Task {self.title}>"
