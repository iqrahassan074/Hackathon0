"""
Authentication routes
Handles user registration, login, and profile management
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token, PasswordChange
from app.services.auth_service import AuthService
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **email**: Valid email address
    - **password**: Password (min 8 characters)
    - **name**: User's full name
    """
    auth_service = AuthService(db)
    user = auth_service.register(user_data)
    return user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login and receive JWT token
    
    - **email**: Registered email
    - **password**: User password
    
    Returns access token valid for 60 minutes
    """
    auth_service = AuthService(db)
    user, access_token = auth_service.login(credentials.email, credentials.password)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=3600,  # 60 minutes in seconds
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    """
    return current_user


@router.put("/password", response_model=UserResponse)
async def change_password(
    password_data: PasswordChange,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Change user password
    
    - **current_password**: Current password
    - **new_password**: New password (min 8 characters)
    """
    auth_service = AuthService(db)
    user = auth_service.change_password(
        current_user,
        password_data.current_password,
        password_data.new_password
    )
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    """
    Logout (client should discard token)
    
    Note: For stateful logout, implement token blacklist
    """
    # For JWT, logout is client-side (discard token)
    # Future: Add token blacklist for immediate invalidation
    return None
