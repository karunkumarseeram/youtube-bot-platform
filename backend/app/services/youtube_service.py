"""
YouTube Service
Python 3.14.3 Compatible
"""

from typing import Optional, List
from sqlalchemy.orm import Session
import logging

from app.models.video import Video
from app.utils.youtube_utils import extract_video_id, get_video_info

logger = logging.getLogger(__name__)


class YouTubeService:
    """Service for managing YouTube videos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def add_video(
        self,
        user_id: int,
        url: str,
        title: Optional[str] = None,
        channel_name: Optional[str] = None
    ) -> Optional[Video]:
        """Add YouTube video to tracking"""
        video_id = extract_video_id(url)
        if not video_id:
            logger.error(f"Invalid YouTube URL: {url}")
            return None
        
        # Check if video already exists
        existing_video = self.db.query(Video).filter(
            Video.video_id == video_id
        ).first()
        
        if existing_video:
            logger.info(f"Video already exists: {video_id}")
            return existing_video
        
        # Get video info if not provided
        if not title or not channel_name:
            info = get_video_info(video_id)
            if info:
                title = title or info.get('title', 'Unknown')
                channel_name = channel_name or info.get('channel', 'Unknown')
        
        video = Video(
            user_id=user_id,
            video_id=video_id,
            title=title or "Unknown",
            url=url,
            channel_name=channel_name or "Unknown",
            current_views=0,
            current_likes=0,
            current_comments=0,
            duration=0
        )
        
        try:
            self.db.add(video)
            self.db.commit()
            self.db.refresh(video)
            logger.info(f"✅ Video added: {video_id}")
            return video
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error adding video: {str(e)}")
            return None
    
    def get_video(self, video_id: int) -> Optional[Video]:
        """Get video by ID"""
        try:
            return self.db.query(Video).filter(Video.id == video_id).first()
        except Exception as e:
            logger.error(f"Error getting video: {str(e)}")
            return None
    
    def get_user_videos(self, user_id: int) -> List[Video]:
        """Get all videos for user"""
        try:
            return self.db.query(Video).filter(Video.user_id == user_id).all()
        except Exception as e:
            logger.error(f"Error getting user videos: {str(e)}")
            return []
    
    def update_video_stats(
        self,
        video_id: int,
        views: int,
        likes: int,
        comments: int
    ) -> Optional[Video]:
        """Update video statistics"""
        try:
            video = self.get_video(video_id)
            if video:
                video.current_views = views
                video.current_likes = likes
                video.current_comments = comments
                self.db.commit()
                self.db.refresh(video)
                return video
        except Exception as e:
            logger.error(f"Error updating video stats: {str(e)}")
            self.db.rollback()
        
        return None