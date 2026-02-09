# backend/app/models/daily_note.py
from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class DailyNote(Base):
    """일일 노트 모델 (Obsidian Daily Notes 스타일)"""
    __tablename__ = "daily_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    date = Column(Date, nullable=False)  # 날짜 (시간 제외)
    content = Column(Text, nullable=True)  # 마크다운 내용
    mood = Column(String(20), nullable=True)  # 'great' | 'good' | 'okay' | 'bad'

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="daily_notes")

    # 제약조건: 한 유저당 하루에 하나의 노트만
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )

    def __repr__(self):
        return f"<DailyNote {self.date}>"
