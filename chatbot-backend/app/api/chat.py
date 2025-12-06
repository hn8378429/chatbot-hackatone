from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.models.schemas import (
    ChatMessage, 
    ChatResponse,
    DocumentIndexRequest,
    DocumentIndexResponse
)
from app.models.database import get_db, ChatHistory, DocumentChunk
from app.services.rag_agent import rag_agent
from app.services.document_processor import doc_processor
from app.services.vector_store import get_vector_store

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Handle chat messages with RAG support.
    Supports answering based on selected text or full book context.
    """
    try:
        # Get recent chat history for context
        recent_chats = db.query(ChatHistory)\
            .filter(ChatHistory.session_id == message.session_id)\
            .order_by(ChatHistory.created_at.desc())\
            .limit(5)\
            .all()
        
        chat_history = [
            {
                "user": chat.user_message,
                "assistant": chat.bot_response
            }
            for chat in reversed(recent_chats)
        ]
        
        # Generate response using RAG
        response_text, context_used = rag_agent.chat(
            user_message=message.message,
            selected_text=message.selected_text,
            chat_history=chat_history
        )
        
        # Save to database
        chat_record = ChatHistory(
            session_id=message.session_id,
            user_message=message.message,
            bot_response=response_text,
            context_used=[
                {
                    "text": ctx["text"][:500],  # Truncate for storage
                    "score": ctx["score"],
                    "source": ctx["metadata"].get("source")
                }
                for ctx in context_used
            ],
            selected_text=message.selected_text
        )
        db.add(chat_record)
        db.commit()
        
        logger.info(f"Chat processed for session: {message.session_id}")
        
        return ChatResponse(
            response=response_text,
            context_used=context_used,
            session_id=message.session_id
        )
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/index", response_model=DocumentIndexResponse)
async def index_document(
    request: DocumentIndexRequest,
    db: Session = Depends(get_db)
):
    """
    Index document content for RAG retrieval.
    Use this to index book chapters/pages.
    """
    try:
        # Process document into chunks
        chunks, metadatas = doc_processor.process_document(
            content=request.content,
            source=request.source,
            metadata=request.metadata
        )
        
        # Add to vector store
        chunk_ids = get_vector_store().add_documents(chunks, metadatas)
        
        # Save metadata to database
        for chunk_id, chunk_text, metadata in zip(chunk_ids, chunks, metadatas):
            doc_chunk = DocumentChunk(
                chunk_id=chunk_id,
                source=request.source,
                content=chunk_text,
                doc_metadata=metadata
            )
            db.add(doc_chunk)
        
        db.commit()
        
        logger.info(f"Indexed {len(chunks)} chunks from {request.source}")
        
        return DocumentIndexResponse(
            message=f"Successfully indexed {len(chunks)} chunks",
            chunks_indexed=len(chunks),
            chunk_ids=chunk_ids
        )
    
    except Exception as e:
        logger.error(f"Error in index endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get chat history for a session"""
    try:
        history = db.query(ChatHistory)\
            .filter(ChatHistory.session_id == session_id)\
            .order_by(ChatHistory.created_at.desc())\
            .limit(limit)\
            .all()
        
        return {
            "session_id": session_id,
            "messages": [
                {
                    "user_message": chat.user_message,
                    "bot_response": chat.bot_response,
                    "created_at": chat.created_at.isoformat(),
                    "context_used": chat.context_used
                }
                for chat in reversed(history)
            ]
        }
    
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
