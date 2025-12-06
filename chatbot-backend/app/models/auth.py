"""
User authentication and profile models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum
from datetime import datetime
from app.models.database import Base
import enum


class ExperienceLevel(str, enum.Enum):
    """Experience level enum"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class User(Base):
    """User model with authentication and profile data"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile Information
    full_name = Column(String(255), nullable=True)
    
    # Background Questions for Personalization
    software_experience = Column(SQLEnum(ExperienceLevel), default=ExperienceLevel.BEGINNER)
    hardware_experience = Column(SQLEnum(ExperienceLevel), default=ExperienceLevel.BEGINNER)
    programming_languages = Column(Text, nullable=True)  # JSON string of languages
    industry_background = Column(String(255), nullable=True)
    learning_goals = Column(Text, nullable=True)
    
    # Preferences
    preferred_language = Column(String(10), default="en")  # en or ur
    content_complexity = Column(String(20), default="auto")  # auto, simple, detailed
    
    # Metadata
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TranslationCache(Base):
    """Cache translations to avoid re-translating"""
    __tablename__ = "translation_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    source_content_hash = Column(String(64), index=True, nullable=False)  # MD5 hash
    source_language = Column(String(10), default="en")
    target_language = Column(String(10), nullable=False)
    translated_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class PersonalizedContent(Base):
    """Store personalized content versions"""
    __tablename__ = "personalized_content"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    chapter_path = Column(String(255), index=True, nullable=False)
    original_content_hash = Column(String(64), nullable=False)
    personalized_content = Column(Text, nullable=False)
    complexity_level = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
