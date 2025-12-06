from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

# Create SQLAlchemy engine
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ChatHistory(Base):
    """Store chat conversation history"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True, nullable=False)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    context_used = Column(JSON, nullable=True)  # Store retrieved context
    selected_text = Column(Text, nullable=True)  # User-selected text for context
    created_at = Column(DateTime, default=datetime.utcnow)


class DocumentChunk(Base):
    """Store metadata about indexed document chunks"""
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(String(255), unique=True, index=True, nullable=False)
    source = Column(String(500), nullable=False)  # Source file/page
    content = Column(Text, nullable=False)
    doc_metadata = Column(JSON, nullable=True)  # Renamed from 'metadata' to avoid SQLAlchemy conflict
    indexed_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
