"""
Authentication service
Handles user registration, login, and token management
"""
from sqlalchemy.orm import Session
from datetime import timedelta
import uuid

from app.models.user import User
from app.schemas.auth import UserCreate
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.error_handler import ConflictException, UnauthorizedException, BadRequestException


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register(self, user_data: UserCreate) -> User:
        """
        Register a new user
        
        Args:
            user_data: User registration data
            
        Returns:
            Created User object
            
        Raises:
            ConflictException: If email already exists
        """
        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ConflictException("Email already registered")
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        db_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            name=user_data.name
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def login(self, email: str, password: str) -> tuple[User, str]:
        """
        Authenticate user and return JWT token
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Tuple of (User, access_token)
            
        Raises:
            UnauthorizedException: If credentials are invalid
        """
        # Find user
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not user.is_active:
            raise UnauthorizedException("Invalid email or password")
        
        # Verify password
        if not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id)}
        )
        
        return user, access_token
    
    def get_user_by_id(self, user_id: uuid.UUID) -> User:
        """
        Get user by ID
        
        Args:
            user_id: User UUID
            
        Returns:
            User object
            
        Raises:
            NotFoundException: If user not found
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            from app.utils.error_handler import NotFoundException
            raise NotFoundException("User not found")
        return user
    
    def change_password(self, user: User, current_password: str, new_password: str) -> User:
        """
        Change user password
        
        Args:
            user: User object
            current_password: Current password
            new_password: New password
            
        Returns:
            Updated User object
            
        Raises:
            BadRequestException: If current password is incorrect
        """
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise BadRequestException("Current password is incorrect")
        
        # Update password
        user.password_hash = hash_password(new_password)
        self.db.commit()
        self.db.refresh(user)
        
        return user
