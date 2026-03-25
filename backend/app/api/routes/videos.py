"""
Videos Routes
Python 3.14.3 Compatible
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.schemas.video import VideoCreate, VideoResponse, VideoUpdate
from app.models.video import Video
from app.services.youtube_service import YouTubeService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
def add_video(
    video: VideoCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Add YouTube video for tracking"""
    youtube_service = YouTubeService(db)
    db_video = youtube_service.add_video(
        user_id=user_id,
        url=video.url,
        title=video.title,
        channel_name=video.channel_name
    )
    
    if not db_video:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL"
        )
    
    return db_video


@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get video details"""
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    return video


@router.get("/user/{user_id}", response_model=List[VideoResponse])
def get_user_videos(user_id: int, db: Session = Depends(get_db)):
    """Get all videos for user"""
    videos = db.query(Video).filter(Video.user_id == user_id).all()
    return videos


@router.put("/{video_id}", response_model=VideoResponse)
def update_video(
    video_id: int,
    video_update: VideoUpdate,
    db: Session = Depends(get_db)
):
    """Update video details"""
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video_update.title:
        video.title = video_update.title
    if video_update.channel_name:
        video.channel_name = video_update.channel_name
    
    try:
        db.commit()
        db.refresh(video)
        return video
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating video: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update video"
        )


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(video_id: int, db: Session = Depends(get_db)):
    """Delete video"""
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    try:
        db.delete(video)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting video: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete video"
        )