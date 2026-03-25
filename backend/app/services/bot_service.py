"""
Bot Service
Python 3.14.3 Compatible
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import logging

from app.models.bot_job import BotJob, BotStatus
from app.models.video import Video

logger = logging.getLogger(__name__)


class BotService:
    """Service for managing bot jobs"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_bot_job(
        self,
        user_id: int,
        video_id: int,
        target_views: int,
        target_likes: int = 0,
        target_comments: int = 0,
        daily_increment: int = 500,
        watch_time_seconds: int = 120,
        engagement_ratio: float = 0.05,
        use_proxy: bool = False
    ) -> Optional[BotJob]:
        """Create new bot job"""
        try:
            video = self.db.query(Video).filter(Video.id == video_id).first()
            if not video:
                logger.error(f"Video not found: {video_id}")
                return None
            
            bot_job = BotJob(
                user_id=user_id,
                video_id=video_id,
                target_views=target_views,
                target_likes=target_likes,
                target_comments=target_comments,
                daily_increment=daily_increment,
                watch_time_seconds=watch_time_seconds,
                engagement_ratio=engagement_ratio,
                use_proxy=use_proxy,
                status=BotStatus.PENDING
            )
            
            self.db.add(bot_job)
            self.db.commit()
            self.db.refresh(bot_job)
            
            logger.info(f"✅ Bot job created: {bot_job.id}")
            return bot_job
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error creating bot job: {str(e)}")
            return None
    
    def get_bot_job(self, job_id: int) -> Optional[BotJob]:
        """Get bot job by ID"""
        try:
            return self.db.query(BotJob).filter(BotJob.id == job_id).first()
        except Exception as e:
            logger.error(f"Error getting bot job: {str(e)}")
            return None
    
    def get_user_bot_jobs(self, user_id: int) -> List[BotJob]:
        """Get all bot jobs for user"""
        try:
            return self.db.query(BotJob).filter(BotJob.user_id == user_id).order_by(BotJob.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting user bot jobs: {str(e)}")
            return []
    
    def start_bot(self, job_id: int) -> Optional[BotJob]:
        """Start bot job"""
        try:
            job = self.get_bot_job(job_id)
            if not job:
                return None
            
            job.status = BotStatus.RUNNING
            job.started_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(job)
            
            logger.info(f"✅ Bot job started: {job_id}")
            return job
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error starting bot: {str(e)}")
            return None
    
    def pause_bot(self, job_id: int) -> Optional[BotJob]:
        """Pause bot job"""
        try:
            job = self.get_bot_job(job_id)
            if job:
                job.status = BotStatus.PAUSED
                self.db.commit()
                self.db.refresh(job)
                logger.info(f"⏸️  Bot job paused: {job_id}")
            return job
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error pausing bot: {str(e)}")
            return None
    
    def stop_bot(self, job_id: int) -> Optional[BotJob]:
        """Stop bot job"""
        try:
            job = self.get_bot_job(job_id)
            if job:
                job.status = BotStatus.STOPPED
                job.completed_at = datetime.now(timezone.utc)
                self.db.commit()
                self.db.refresh(job)
                logger.info(f"🛑 Bot job stopped: {job_id}")
            return job
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error stopping bot: {str(e)}")
            return None
    
    def update_bot_progress(
        self,
        job_id: int,
        views: int,
        likes: int,
        comments: int
    ) -> Optional[BotJob]:
        """Update bot job progress"""
        try:
            job = self.get_bot_job(job_id)
            if job:
                job.current_views = views
                job.current_likes = likes
                job.current_comments = comments
                
                # Check if target reached
                if views >= job.target_views:
                    job.status = BotStatus.COMPLETED
                    job.completed_at = datetime.now(timezone.utc)
                    logger.info(f"✅ Bot job completed: {job_id}")
                
                self.db.commit()
                self.db.refresh(job)
            
            return job
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error updating bot progress: {str(e)}")
            return None