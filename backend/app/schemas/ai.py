"""
AI schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class AIRecommendRequest(BaseModel):
    """Schema for requesting AI recommendations"""
    context: Optional[str] = Field(None, description="Additional context for recommendations")
    task_ids: Optional[List[uuid.UUID]] = Field(None, description="Specific tasks to analyze")


class AIRecommendationItem(BaseModel):
    """Single recommendation item"""
    id: uuid.UUID
    task_id: Optional[uuid.UUID]
    recommendation_text: str
    confidence_score: Optional[float]
    is_accepted: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class AIRecommendResponse(BaseModel):
    """Schema for AI recommendation response"""
    recommendations: List[str]
    message: str
    history: Optional[List[AIRecommendationItem]] = None


class AIOptimizeRequest(BaseModel):
    """Schema for task optimization request"""
    task_id: uuid.UUID
    focus_areas: Optional[List[str]] = Field(None, description="Areas to focus on: clarity, priority, breakdown")
