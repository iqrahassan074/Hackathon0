"""
Task service
Handles task CRUD operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.error_handler import NotFoundException, ForbiddenException


class TaskService:
    """Service for task operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_task(self, user: User, task_data: TaskCreate) -> Task:
        """
        Create a new task for the user
        
        Args:
            user: User creating the task
            task_data: Task creation data
            
        Returns:
            Created Task object
        """
        db_task = Task(
            user_id=user.id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status.value,
            priority=task_data.priority.value,
            due_date=task_data.due_date
        )
        
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        
        return db_task
    
    def get_tasks(
        self,
        user: User,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
        priority: Optional[str] = None
    ) -> List[Task]:
        """
        Get tasks for a user with optional filtering
        
        Args:
            user: User object
            skip: Number of tasks to skip (pagination)
            limit: Maximum number of tasks to return
            status: Optional status filter
            priority: Optional priority filter
            
        Returns:
            List of Task objects
        """
        query = self.db.query(Task).filter(Task.user_id == user.id)
        
        if status:
            query = query.filter(Task.status == status.value)
        if priority:
            query = query.filter(Task.priority == priority)
        
        tasks = query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
        
        return tasks
    
    def get_task(self, user: User, task_id: uuid.UUID) -> Task:
        """
        Get a specific task by ID
        
        Args:
            user: User object (for ownership verification)
            task_id: Task UUID
            
        Returns:
            Task object
            
        Raises:
            NotFoundException: If task not found
            ForbiddenException: If task doesn't belong to user
        """
        task = self.db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise NotFoundException("Task not found")
        
        if task.user_id != user.id:
            raise ForbiddenException("You don't have access to this task")
        
        return task
    
    def update_task(self, user: User, task_id: uuid.UUID, task_data: TaskUpdate) -> Task:
        """
        Update a task
        
        Args:
            user: User object
            task_id: Task UUID
            task_data: Task update data
            
        Returns:
            Updated Task object
            
        Raises:
            NotFoundException: If task not found
            ForbiddenException: If task doesn't belong to user
        """
        task = self.get_task(user, task_id)
        
        # Update only provided fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(task, field):
                setattr(task, field, value)
        
        task.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def delete_task(self, user: User, task_id: uuid.UUID) -> bool:
        """
        Delete a task
        
        Args:
            user: User object
            task_id: Task UUID
            
        Returns:
            True if deleted successfully
            
        Raises:
            NotFoundException: If task not found
            ForbiddenException: If task doesn't belong to user
        """
        task = self.get_task(user, task_id)
        
        self.db.delete(task)
        self.db.commit()
        
        return True
    
    def mark_task_complete(self, user: User, task_id: uuid.UUID) -> Task:
        """
        Mark a task as complete
        
        Args:
            user: User object
            task_id: Task UUID
            
        Returns:
            Updated Task object
            
        Raises:
            NotFoundException: If task not found
            ForbiddenException: If task doesn't belong to user
        """
        task = self.get_task(user, task_id)
        
        task.status = TaskStatus.completed.value
        task.completed_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def get_task_stats(self, user: User) -> dict:
        """
        Get task statistics for a user
        
        Args:
            user: User object
            
        Returns:
            Dictionary with task statistics
        """
        total = self.db.query(Task).filter(Task.user_id == user.id).count()
        pending = self.db.query(Task).filter(
            Task.user_id == user.id,
            Task.status == TaskStatus.pending.value
        ).count()
        in_progress = self.db.query(Task).filter(
            Task.user_id == user.id,
            Task.status == TaskStatus.in_progress.value
        ).count()
        completed = self.db.query(Task).filter(
            Task.user_id == user.id,
            Task.status == TaskStatus.completed.value
        ).count()
        
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed
        }
