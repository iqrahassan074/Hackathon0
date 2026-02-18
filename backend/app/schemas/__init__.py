"""
Pydantic Schemas
All request/response schemas for API validation
"""
from app.schemas.auth import (
    UserCreate, UserLogin, UserResponse, Token, PasswordChange
)
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority
)
from app.schemas.setting import (
    SettingCreate, SettingUpdate, SettingResponse
)
from app.schemas.ai import (
    AIRecommendRequest, AIRecommendResponse, AIOptimizeRequest
)

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "Token", "PasswordChange",
    "TaskCreate", "TaskUpdate", "TaskResponse", "TaskStatus", "TaskPriority",
    "SettingCreate", "SettingUpdate", "SettingResponse",
    "AIRecommendRequest", "AIRecommendResponse", "AIOptimizeRequest"
]
