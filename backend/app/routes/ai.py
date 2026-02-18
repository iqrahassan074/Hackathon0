"""
AI routes
Handles AI-powered features and recommendations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional
import uuid

from app.database import get_db
from app.schemas.ai import (
    AIRecommendRequest,
    AIRecommendResponse,
    AIOptimizeRequest,
    AIRecommendationItem
)
from app.services.ai_service import AIService
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/recommend", response_model=AIRecommendResponse)
async def get_recommendations(
    request: AIRecommendRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Get AI-powered task recommendations
    
    - **context**: Optional additional context for recommendations
    - **task_ids**: Optional list of specific task IDs to analyze
    
    Returns personalized recommendations based on user's tasks
    """
    ai_service = AIService(db)
    
    recommendations = ai_service.get_task_recommendations(
        current_user,
        context=request.context,
        task_ids=request.task_ids
    )
    
    return AIRecommendResponse(
        recommendations=recommendations,
        message=f"Generated {len(recommendations)} recommendations"
    )


@router.post("/optimize")
async def optimize_task(
    request: AIOptimizeRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Get AI optimization suggestions for a specific task
    
    - **task_id**: ID of the task to optimize
    - **focus_areas**: Optional areas to focus on (clarity, priority, breakdown)
    
    Returns detailed optimization suggestions
    """
    ai_service = AIService(db)
    
    result = ai_service.optimize_task(
        current_user,
        request.task_id,
        request.focus_areas
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=result.get("error", "AI service unavailable")
        )
    
    return result


@router.get("/history", response_model=List[AIRecommendationItem])
async def get_ai_history(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    limit: int = 50
):
    """
    Get AI recommendation history
    
    - **limit**: Maximum number of records to return (default 50)
    
    Returns historical AI recommendations for the user
    """
    ai_service = AIService(db)
    history = ai_service.get_history(current_user, limit=limit)
    
    return [
        AIRecommendationItem(
            id=rec.id,
            task_id=rec.task_id,
            recommendation_text=rec.recommendation_text,
            confidence_score=float(rec.confidence_score) if rec.confidence_score else None,
            is_accepted=rec.is_accepted,
            created_at=rec.created_at
        )
        for rec in history
    ]


@router.post("/history/{recommendation_id}/accept")
async def accept_recommendation(
    recommendation_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Mark a recommendation as accepted
    
    Use this to track which recommendations were useful
    """
    ai_service = AIService(db)
    
    success = ai_service.accept_recommendation(current_user, recommendation_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    return {"message": "Recommendation marked as accepted"}
