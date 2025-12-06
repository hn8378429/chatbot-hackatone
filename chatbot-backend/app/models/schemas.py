from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Chat message from user"""
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: str = Field(..., min_length=1, max_length=255)
    selected_text: Optional[str] = Field(None, max_length=10000)


class ChatResponse(BaseModel):
    """Response from chatbot"""
    response: str
    context_used: Optional[List[Dict[str, Any]]] = None
    session_id: str


class DocumentIndexRequest(BaseModel):
    """Request to index document content"""
    content: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1, max_length=500)
    metadata: Optional[Dict[str, Any]] = None


class DocumentIndexResponse(BaseModel):
    """Response after indexing"""
    message: str
    chunks_indexed: int
    chunk_ids: List[str]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    services: Dict[str, bool]
