"""
Video Schemas (Pydantic Models)
Python 3.14.3 Compatible
"""

from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional


class VideoCreate(BaseModel):
    """Video Creation Schema"""
    url: str = Field(..., description="YouTube Video URL")
    title: Optional[str] = Field(None, max_length=500)
    channel_name: Optional[str] = Field(None, max_length=200)

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "title": "Video Title",
                "channel_name": "Channel Name"
            }
        }


class VideoUpdate(BaseModel):
    """Video Update Schema"""
    title: Optional[str] = Field(None, max_length=500)
    channel_name: Optional[str] = Field(None, max_length=200)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Title",
                "channel_name": "Updated Channel"
            }
        }


class VideoResponse(BaseModel):
    """Video Response Schema"""
    id: int
    video_id: str
    title: str
    url: str
    channel_name: str
    current_views: int
    current_likes: int
    current_comments: int
    duration: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "video_id": "dQw4w9WgXcQ",
                "title": "Video Title",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "channel_name": "Channel Name",
                "current_views": 1000,
                "current_likes": 50,
                "current_comments": 10,
                "duration": 213,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }