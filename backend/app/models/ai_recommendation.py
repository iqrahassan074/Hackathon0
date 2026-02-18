"""
AI Recommendation model for storing AI-generated suggestions
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class AIRecommendation(Base):
    """AIRecommendation model storing AI-generated task recommendations"""
    
    __tablename__ = "ai_recommendations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    recommendation_text = Column(Text, nullable=False)
    confidence_score = Column(Numeric(3, 2), nullable=True)  # 0.00 to 1.00
    context = Column(Text, nullable=True)  # Store as JSON string for SQLite compatibility
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="ai_recommendations")
    task = relationship("Task", back_populates="ai_recommendations")
    
    def __repr__(self):
        return f"<AIRecommendation {self.id}>"
