"""
Content personalization and translation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.auth import User
from app.models.auth_schemas import PersonalizeRequest, PersonalizeResponse, TranslateRequest, TranslateResponse
from app.services.auth import get_current_user, get_current_user_optional
from app.services.personalization import personalization_service
from app.services.translation import translation_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/content", tags=["content"])


@router.post("/personalize", response_model=PersonalizeResponse)
async def personalize_content(
    request: PersonalizeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Personalize content based on user's background and experience level.
    Requires authentication.
    """
    try:
        result = personalization_service.personalize_content(
            content=request.content,
            user=current_user,
            chapter_path=request.chapter_path,
            db=db
        )
        
        return PersonalizeResponse(**result)
    except Exception as e:
        logger.error(f"Personalization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate", response_model=TranslateResponse)
async def translate_content(
    request: TranslateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """
    Translate content to specified language (default: Urdu).
    Works for both authenticated and non-authenticated users.
    """
    try:
        result = translation_service.translate(
            content=request.content,
            target_language=request.target_language,
            source_language=request.source_language,
            db=db
        )
        
        return TranslateResponse(**result)
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
