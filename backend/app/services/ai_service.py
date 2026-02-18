"""
AI Service
Handles AI-powered task recommendations and optimization
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import uuid
import json
import structlog
from datetime import datetime

from app.models.user import User
from app.models.task import Task
from app.models.ai_recommendation import AIRecommendation
from app.services.ai_cli_wrapper import AICLIWrapper
from app.config import get_settings

logger = structlog.get_logger(__name__)


class AIService:
    """Service for AI-powered features"""
    
    def __init__(self, db: Session):
        self.db = db
        self.cli_wrapper = AICLIWrapper()
        self.settings = get_settings()
    
    def _build_task_context(self, user: User, task_ids: Optional[List[uuid.UUID]] = None) -> str:
        """
        Build context string from user's tasks
        
        Args:
            user: User object
            task_ids: Optional list of specific task IDs to include
            
        Returns:
            Context string for AI
        """
        query = self.db.query(Task).filter(Task.user_id == user.id)
        
        if task_ids:
            query = query.filter(Task.id.in_(task_ids))
        
        tasks = query.order_by(Task.created_at.desc()).limit(20).all()
        
        context_parts = []
        for task in tasks:
            context_parts.append(
                f"- {task.title} (Status: {task.status}, Priority: {task.priority})"
            )
            if task.description:
                context_parts.append(f"  Description: {task.description}")
        
        return "\n".join(context_parts)
    
    def get_task_recommendations(
        self,
        user: User,
        context: Optional[str] = None,
        task_ids: Optional[List[uuid.UUID]] = None
    ) -> List[str]:
        """
        Get AI-powered task recommendations
        
        Args:
            user: User object
            context: Optional additional context
            task_ids: Optional specific tasks to analyze
            
        Returns:
            List of recommendation strings
        """
        # Build prompt
        task_context = self._build_task_context(user, task_ids)
        
        prompt = f"""Analyze these tasks and provide 3-5 actionable recommendations to improve productivity:

{task_context}

Additional context: {context or 'None'}

Provide recommendations in this format:
1. [Recommendation title]: [Description]
2. [Recommendation title]: [Description]
...

Focus on:
- Priority optimization
- Task grouping
- Time management
- Goal alignment"""

        # Call AI
        response = self.cli_wrapper.call_ai(prompt)
        
        if not response:
            # Fallback recommendations if AI unavailable
            return self._get_fallback_recommendations(user)
        
        # Parse response
        recommendations = self.cli_wrapper.parse_recommendations(response)
        
        # Store in database
        self._store_recommendations(user, recommendations, context=json.dumps({
            "task_ids": [str(tid) for tid in task_ids] if task_ids else None,
            "additional_context": context
        }))
        
        return recommendations
    
    def optimize_task(self, user: User, task_id: uuid.UUID, focus_areas: Optional[List[str]] = None) -> Dict:
        """
        Get AI optimization suggestions for a specific task
        
        Args:
            user: User object
            task_id: Task to optimize
            focus_areas: Optional areas to focus on
            
        Returns:
            Dictionary with optimization suggestions
        """
        task = self.db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
        if not task:
            return {"error": "Task not found"}
        
        focus = ", ".join(focus_areas) if focus_areas else "clarity, priority, breakdown"
        
        prompt = f"""Optimize this task for better clarity and actionability:

Title: {task.title}
Description: {task.description or 'No description'}
Status: {task.status}
Priority: {task.priority}
Due Date: {task.due_date or 'Not set'}

Focus areas: {focus}

Provide suggestions for:
1. Title improvement
2. Description enhancement
3. Priority assessment
4. Task breakdown (if applicable)
5. Next actions"""

        response = self.cli_wrapper.call_ai(prompt)
        
        if not response:
            return {
                "error": "AI service unavailable",
                "fallback": {
                    "title": task.title,
                    "suggestions": [
                        "Add more specific details to the description",
                        "Consider breaking into smaller subtasks",
                        "Set a clear due date if applicable"
                    ]
                }
            }
        
        return {
            "task_id": str(task_id),
            "suggestions": response,
            "parsed": self.cli_wrapper.parse_recommendations(response)
        }
    
    def _get_fallback_recommendations(self, user: User) -> List[str]:
        """
        Get fallback recommendations when AI is unavailable
        
        Args:
            user: User object
            
        Returns:
            List of generic recommendations
        """
        stats = self.db.query(Task).filter(Task.user_id == user.id).all()
        total = len(stats)
        pending = len([t for t in stats if t.status == "pending"])
        
        return [
            f"You have {pending} pending tasks out of {total} total",
            "Consider completing high-priority tasks first",
            "Break large tasks into smaller, actionable steps",
            "Set specific due dates for better time management",
            "Review and update task priorities regularly"
        ]
    
    def _store_recommendations(
        self,
        user: User,
        recommendations: List[str],
        context: Optional[str] = None
    ):
        """
        Store recommendations in database
        
        Args:
            user: User object
            recommendations: List of recommendation strings
            context: Optional context JSON
        """
        for rec_text in recommendations:
            db_rec = AIRecommendation(
                user_id=user.id,
                recommendation_text=rec_text,
                context=context
            )
            self.db.add(db_rec)
        
        try:
            self.db.commit()
            logger.info("recommendations_stored", count=len(recommendations), user_id=str(user.id))
        except Exception as e:
            self.db.rollback()
            logger.exception("recommendations_store_failed", error=str(e))
    
    def get_history(self, user: User, limit: int = 50) -> List[AIRecommendation]:
        """
        Get AI recommendation history for user
        
        Args:
            user: User object
            limit: Maximum number of records to return
            
        Returns:
            List of AIRecommendation objects
        """
        return self.db.query(AIRecommendation).filter(
            AIRecommendation.user_id == user.id
        ).order_by(
            AIRecommendation.created_at.desc()
        ).limit(limit).all()
    
    def accept_recommendation(self, user: User, recommendation_id: uuid.UUID) -> bool:
        """
        Mark a recommendation as accepted
        
        Args:
            user: User object
            recommendation_id: Recommendation UUID
            
        Returns:
            True if successful
        """
        rec = self.db.query(AIRecommendation).filter(
            AIRecommendation.id == recommendation_id,
            AIRecommendation.user_id == user.id
        ).first()
        
        if rec:
            rec.is_accepted = True
            self.db.commit()
            return True
        
        return False
