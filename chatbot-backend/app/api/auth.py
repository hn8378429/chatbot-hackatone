"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.auth import User
from app.models.auth_schemas import UserSignup, UserLogin, Token, UserProfile, UserUpdate
from app.services.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    Register a new user with background information for personalization
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    programming_langs = json.dumps(user_data.programming_languages) if user_data.programming_languages else None
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        software_experience=user_data.software_experience,
        hardware_experience=user_data.hardware_experience,
        programming_languages=programming_langs,
        industry_background=user_data.industry_background,
        learning_goals=user_data.learning_goals
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"New user registered: {new_user.email}")
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.id})
    
    return Token(
        access_token=access_token,
        user=UserProfile.from_orm(new_user)
    )


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password
    """
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    logger.info(f"User logged in: {user.email}")
    
    return Token(
        access_token=access_token,
        user=UserProfile.from_orm(user)
    )


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    """
    return UserProfile.from_orm(current_user)


@router.put("/me", response_model=UserProfile)
async def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile and preferences
    """
    # Update fields
    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name
    if update_data.software_experience is not None:
        current_user.software_experience = update_data.software_experience
    if update_data.hardware_experience is not None:
        current_user.hardware_experience = update_data.hardware_experience
    if update_data.programming_languages is not None:
        current_user.programming_languages = json.dumps(update_data.programming_languages)
    if update_data.industry_background is not None:
        current_user.industry_background = update_data.industry_background
    if update_data.learning_goals is not None:
        current_user.learning_goals = update_data.learning_goals
    if update_data.preferred_language is not None:
        current_user.preferred_language = update_data.preferred_language
    if update_data.content_complexity is not None:
        current_user.content_complexity = update_data.content_complexity
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"User profile updated: {current_user.email}")
    
    return UserProfile.from_orm(current_user)
