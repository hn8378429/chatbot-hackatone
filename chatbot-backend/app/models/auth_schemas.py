"""
Pydantic schemas for authentication and user profiles
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class UserSignup(BaseModel):
    """User signup request"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    
    # Background questions
    software_experience: ExperienceLevel = ExperienceLevel.BEGINNER
    hardware_experience: ExperienceLevel = ExperienceLevel.BEGINNER
    programming_languages: Optional[List[str]] = []
    industry_background: Optional[str] = None
    learning_goals: Optional[str] = None


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: "UserProfile"


class UserProfile(BaseModel):
    """User profile response"""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    software_experience: str
    hardware_experience: str
    programming_languages: Optional[str]
    industry_background: Optional[str]
    learning_goals: Optional[str]
    preferred_language: str
    content_complexity: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Update user profile"""
    full_name: Optional[str] = None
    software_experience: Optional[ExperienceLevel] = None
    hardware_experience: Optional[ExperienceLevel] = None
    programming_languages: Optional[List[str]] = None
    industry_background: Optional[str] = None
    learning_goals: Optional[str] = None
    preferred_language: Optional[str] = None
    content_complexity: Optional[str] = None


class PersonalizeRequest(BaseModel):
    """Request to personalize content"""
    chapter_path: str
    content: str
    user_experience: str


class PersonalizeResponse(BaseModel):
    """Personalized content response"""
    personalized_content: str
    complexity_level: str
    cached: bool = False


class TranslateRequest(BaseModel):
    """Request to translate content"""
    content: str
    target_language: str = "ur"
    source_language: str = "en"


class TranslateResponse(BaseModel):
    """Translation response"""
    translated_content: str
    cached: bool = False
