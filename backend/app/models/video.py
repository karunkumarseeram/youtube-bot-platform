"""
Video Model
Python 3.14.3 Compatible
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Video(Base):
    """Video Database Model"""
    
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    video_id = Column(String(20), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(String(500), unique=True, nullable=False)
    channel_name = Column(String(200), nullable=False)
    current_views = Column(Integer, default=0, index=True)
    current_likes = Column(Integer, default=0)
    current_comments = Column(Integer, default=0)
    duration = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    owner = relationship("User", back_populates="videos")
    bot_jobs = relationship("BotJob", back_populates="video", cascade="all, delete-orphan")
    metrics = relationship("Metrics", back_populates="video", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_user_video', 'user_id', 'video_id'),
    )

    def __repr__(self) -> str:
        return f"<Video {self.video_id}>"
    
    def __str__(self) -> str:
        return f"Video({self.video_id}, {self.title})"