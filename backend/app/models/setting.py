"""
Setting model for user preferences
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Setting(Base):
    """Setting model representing user preferences and configuration"""
    
    __tablename__ = "settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    theme = Column(String(20), default="light")
    notifications_enabled = Column(Boolean, default=True)
    ai_assistant_enabled = Column(Boolean, default=True)
    ai_provider = Column(String(50), default="claude")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="setting")
    
    def __repr__(self):
        return f"<Setting {self.user_id}>"
