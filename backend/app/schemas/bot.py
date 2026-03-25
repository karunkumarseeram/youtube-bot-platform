"""
Bot Job Schemas (Pydantic Models)
Python 3.14.3 Compatible
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.bot_job import BotStatus


class BotJobCreate(BaseModel):
    """Bot Job Creation Schema"""
    video_id: int = Field(..., gt=0)
    target_views: int = Field(..., gt=0, le=1000000)
    target_likes: int = Field(0, ge=0, le=100000)
    target_comments: int = Field(0, ge=0, le=50000)
    daily_increment: int = Field(500, gt=0, le=100000)
    watch_time_seconds: int = Field(120, gt=0, le=3600)
    engagement_ratio: float = Field(0.05, ge=0.0, le=1.0)
    use_proxy: bool = Field(False)

    class Config:
        json_schema_extra = {
            "example": {
                "video_id": 1,
                "target_views": 10000,
                "target_likes": 500,
                "target_comments": 100,
                "daily_increment": 1000,
                "watch_time_seconds": 120,
                "engagement_ratio": 0.05,
                "use_proxy": False
            }
        }


class BotJobUpdate(BaseModel):
    """Bot Job Update Schema"""
    target_views: Optional[int] = Field(None, gt=0)
    daily_increment: Optional[int] = Field(None, gt=0)
    watch_time_seconds: Optional[int] = Field(None, gt=0)
    engagement_ratio: Optional[float] = Field(None, ge=0.0, le=1.0)

    class Config:
        json_schema_extra = {
            "example": {
                "target_views": 15000,
                "daily_increment": 1500
            }
        }


class BotJobResponse(BaseModel):
    """Bot Job Response Schema"""
    id: int
    video_id: int
    task_id: Optional[str] = None
    target_views: int
    current_views: int
    current_likes: int
    current_comments: int
    status: BotStatus
    daily_increment: int
    watch_time_seconds: int
    engagement_ratio: float
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "video_id": 1,
                "task_id": "task-123",
                "target_views": 10000,
                "current_views": 5000,
                "current_likes": 250,
                "current_comments": 50,
                "status": "running",
                "daily_increment": 1000,
                "watch_time_seconds": 120,
                "engagement_ratio": 0.05,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
                "started_at": "2024-01-15T10:31:00",
                "completed_at": None,
                "error_message": None
            }
        }