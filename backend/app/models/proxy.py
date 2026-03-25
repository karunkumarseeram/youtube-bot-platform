"""
Proxy Server Model
Python 3.14.3 Compatible
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index
from datetime import datetime, timezone
from app.database import Base


class ProxyServer(Base):
    """Proxy Server Database Model"""
    
    __tablename__ = "proxy_servers"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(50), unique=True, index=True, nullable=False)
    port = Column(Integer, nullable=False)
    protocol = Column(String(10), default="http")
    is_active = Column(Boolean, default=True, index=True)
    is_working = Column(Boolean, default=True, index=True)
    last_checked = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_active_working', 'is_active', 'is_working'),
    )

    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.ip}:{self.port}"

    def __repr__(self) -> str:
        return f"<ProxyServer {self.ip}:{self.port}>"
    
    def __str__(self) -> str:
        return f"{self.protocol}://{self.ip}:{self.port}"