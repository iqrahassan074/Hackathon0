"""
Settings routes
Handles user preferences and configuration
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.schemas.setting import SettingCreate, SettingUpdate, SettingResponse
from app.models.user import User
from app.models.setting import Setting
from app.utils.security import get_current_user

router = APIRouter()


def get_or_create_setting(db: Session, user: User) -> Setting:
    """Get existing setting or create default one"""
    setting = db.query(Setting).filter(Setting.user_id == user.id).first()
    
    if not setting:
        setting = Setting(user_id=user.id)
        db.add(setting)
        db.commit()
        db.refresh(setting)
    
    return setting


@router.get("/", response_model=SettingResponse)
async def get_settings(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Get current user's settings
    
    Returns user preferences for theme, notifications, and AI assistant
    """
    setting = get_or_create_setting(db, current_user)
    return setting


@router.put("/", response_model=SettingResponse)
async def update_settings(
    setting_data: SettingUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Update user settings
    
    All fields are optional - only provided fields will be updated
    """
    setting = get_or_create_setting(db, current_user)
    
    # Update only provided fields
    update_data = setting_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(setting, field):
            setattr(setting, field, value)
    
    db.commit()
    db.refresh(setting)
    
    return setting
