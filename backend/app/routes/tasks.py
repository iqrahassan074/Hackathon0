"""
Task routes
Handles CRUD operations for tasks
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
import uuid

from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority
from app.services.task_service import TaskService
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Create a new task
    
    - **title**: Task title (required, max 200 chars)
    - **description**: Task description (optional)
    - **status**: Task status (pending, in_progress, completed)
    - **priority**: Task priority (low, medium, high)
    - **due_date**: Optional due date
    """
    task_service = TaskService(db)
    task = task_service.create_task(current_user, task_data)
    return task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    priority: Optional[str] = None
):
    """
    Get all tasks for current user
    
    - **skip**: Number of tasks to skip (pagination)
    - **limit**: Maximum tasks to return (1-1000)
    - **status**: Filter by status (optional)
    - **priority**: Filter by priority (optional)
    """
    task_service = TaskService(db)
    tasks = task_service.get_tasks(
        current_user,
        skip=skip,
        limit=limit,
        status=status_filter,
        priority=priority
    )
    return tasks


@router.get("/stats")
async def get_task_stats(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Get task statistics for current user
    
    Returns counts for total, pending, in_progress, and completed tasks
    """
    task_service = TaskService(db)
    stats = task_service.get_task_stats(current_user)
    return stats


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID
    """
    task_service = TaskService(db)
    task = task_service.get_task(current_user, task_id)
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: uuid.UUID,
    task_data: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Update a task
    
    All fields are optional - only provided fields will be updated
    """
    task_service = TaskService(db)
    task = task_service.update_task(current_user, task_id, task_data)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Delete a task
    """
    task_service = TaskService(db)
    task_service.delete_task(current_user, task_id)
    return None


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_complete(
    task_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Mark a task as complete
    """
    task_service = TaskService(db)
    task = task_service.mark_task_complete(current_user, task_id)
    return task
