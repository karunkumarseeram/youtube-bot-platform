"""
Metrics Model
Python 3.14.3 Compatible
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Metrics(Base):
    """Metrics Database Model"""
    
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False, index=True)
    
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    watch_time = Column(Float, default=0.0)
    
    average_view_duration = Column(Float, default=0.0)
    engagement_rate = Column(Float, default=0.0)
    
    timestamp = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), index=True)

    # Relationships
    video = relationship("Video", back_populates="metrics")

    # Indexes
    __table_args__ = (
        Index('idx_video_timestamp', 'video_id', 'timestamp'),
    )

    def __repr__(self) -> str:
        return f"<Metrics {self.id}>"
    
    def __str__(self) -> str:
        return f"Metrics({self.video_id}, {self.views} views, {self.engagement_rate:.2%} engagement)"