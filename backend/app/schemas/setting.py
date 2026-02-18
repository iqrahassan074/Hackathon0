"""
Setting schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class SettingCreate(BaseModel):
    """Schema for creating settings"""
    theme: str = Field("light", pattern="^(light|dark|system)$")
    notifications_enabled: bool = True
    ai_assistant_enabled: bool = True
    ai_provider: str = Field("claude", pattern="^(claude|qwen)$")


class SettingUpdate(BaseModel):
    """Schema for updating settings (all fields optional)"""
    theme: Optional[str] = Field(None, pattern="^(light|dark|system)$")
    notifications_enabled: Optional[bool] = None
    ai_assistant_enabled: Optional[bool] = None
    ai_provider: Optional[str] = Field(None, pattern="^(claude|qwen)$")


class SettingResponse(BaseModel):
    """Schema for settings response"""
    id: uuid.UUID
    user_id: uuid.UUID
    theme: str
    notifications_enabled: bool
    ai_assistant_enabled: bool
    ai_provider: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
