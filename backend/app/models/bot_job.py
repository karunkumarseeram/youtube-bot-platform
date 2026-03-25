"""
Bot Job Model
Python 3.14.3 Compatible
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from app.database import Base


class BotStatus(str, enum.Enum):
    """Bot Job Status Enum"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


class BotJob(Base):
    """Bot Job Database Model"""
    
    __tablename__ = "bot_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False, index=True)
    task_id = Column(String(100), unique=True, nullable=True)
    
    # Target metrics
    target_views = Column(Integer, nullable=False)
    target_likes = Column(Integer, default=0)
    target_comments = Column(Integer, default=0)
    
    # Current progress
    current_views = Column(Integer, default=0, index=True)
    current_likes = Column(Integer, default=0)
    current_comments = Column(Integer, default=0)
    
    # Configuration
    daily_increment = Column(Integer, default=500)
    watch_time_seconds = Column(Integer, default=120)
    engagement_ratio = Column(Float, default=0.05)
    use_proxy = Column(Boolean, default=False)
    
    # Status
    status = Column(Enum(BotStatus), default=BotStatus.PENDING, index=True)
    error_message = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    owner = relationship("User", back_populates="bot_jobs")
    video = relationship("Video", back_populates="bot_jobs")

    # Indexes
    __table_args__ = (
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_video_status', 'video_id', 'status'),
    )

    def __repr__(self) -> str:
        return f"<BotJob {self.id}>"
    
    def __str__(self) -> str:
        return f"BotJob({self.id}, {self.status.value}, {self.current_views}/{self.target_views})"