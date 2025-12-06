"""
Translation service for Urdu localization
"""
import logging
import hashlib
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.auth import TranslationCache
from app.config import settings
from openai import OpenAI

logger = logging.getLogger(__name__)


class TranslationService:
    """Service for translating content to Urdu"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if not settings.demo_mode else None
    
    def _get_content_hash(self, content: str) -> str:
        """Generate hash of content for caching"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def translate(
        self,
        content: str,
        target_language: str = "ur",
        source_language: str = "en",
        db: Session = None
    ) -> Dict[str, Any]:
        """Translate content to target language"""
        
        # Check cache first if db provided
        if db:
            content_hash = self._get_content_hash(content)
            cached = db.query(TranslationCache).filter(
                TranslationCache.source_content_hash == content_hash,
                TranslationCache.source_language == source_language,
                TranslationCache.target_language == target_language
            ).first()
            
            if cached:
                logger.info(f"Using cached translation {source_language}->{target_language}")
                return {
                    "translated_content": cached.translated_content,
                    "cached": True
                }
        
        # Translate
        if settings.demo_mode:
            translated = self._demo_translate(content, target_language)
        else:
            translated = self._ai_translate(content, target_language, source_language)
        
        # Cache if db provided
        if db:
            new_cache = TranslationCache(
                source_content_hash=content_hash,
                source_language=source_language,
                target_language=target_language,
                translated_content=translated
            )
            db.add(new_cache)
            db.commit()
        
        logger.info(f"Translated content {source_language}->{target_language}")
        
        return {
            "translated_content": translated,
            "cached": False
        }
    
    def _demo_translate(self, content: str, target_language: str) -> str:
        """Demo translation without AI"""
        if target_language == "ur":
            return f"""
# ترجمہ شدہ مواد (Demo Mode)

**اردو میں ترجمہ**

{content}

---
*یہ ڈیمو موڈ ترجمہ ہے۔ OpenAI کریڈٹس شامل کریں تاکہ حقیقی اردو ترجمہ حاصل کیا جا سکے۔*

**اصل انگریزی:**
{content[:200]}...
"""
        return content
    
    def _ai_translate(self, content: str, target_language: str, source_language: str) -> str:
        """AI-powered translation"""
        try:
            lang_names = {
                "ur": "Urdu (اردو)",
                "en": "English"
            }
            
            target_lang_name = lang_names.get(target_language, target_language)
            
            system_prompt = f"""You are a professional translator specializing in technical documentation.
Translate the following technical content from {source_language} to {target_lang_name}.

Requirements:
1. Maintain markdown formatting
2. Keep code snippets and technical terms in English
3. Translate explanatory text accurately
4. Preserve headings, lists, and structure
5. Use appropriate technical terminology in {target_lang_name}
6. Maintain the same tone and style

For Urdu translations:
- Use proper Urdu technical vocabulary
- Right-to-left formatting will be handled by the frontend
- Keep proper nouns and product names in English"""
            
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate this content:\n\n{content}"}
                ],
                temperature=0.3,  # Lower temperature for more accurate translations
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI translation failed: {e}")
            return self._demo_translate(content, target_language)


translation_service = TranslationService()
