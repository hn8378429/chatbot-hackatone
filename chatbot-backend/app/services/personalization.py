"""
Content personalization service using AI
"""
from typing import Dict, Any
import logging
import hashlib
from sqlalchemy.orm import Session
from app.models.auth import PersonalizedContent, User
from app.config import settings
from openai import OpenAI

logger = logging.getLogger(__name__)


class PersonalizationService:
    """Service for personalizing content based on user background"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if not settings.demo_mode else None
    
    def _get_content_hash(self, content: str) -> str:
        """Generate hash of content for caching"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _determine_complexity(self, user: User) -> str:
        """Determine appropriate complexity level for user"""
        # Auto-determine based on experience
        if user.content_complexity != "auto":
            return user.content_complexity
        
        # Calculate average experience
        exp_levels = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
        avg_exp = (exp_levels.get(user.software_experience, 1) + 
                   exp_levels.get(user.hardware_experience, 1)) / 2
        
        if avg_exp >= 3.5:
            return "expert"
        elif avg_exp >= 2.5:
            return "advanced"
        elif avg_exp >= 1.5:
            return "intermediate"
        else:
            return "beginner"
    
    def personalize_content(
        self,
        content: str,
        user: User,
        chapter_path: str,
        db: Session
    ) -> Dict[str, Any]:
        """Personalize content based on user profile"""
        
        # Check cache first
        content_hash = self._get_content_hash(content)
        complexity = self._determine_complexity(user)
        
        cached = db.query(PersonalizedContent).filter(
            PersonalizedContent.user_id == user.id,
            PersonalizedContent.chapter_path == chapter_path,
            PersonalizedContent.original_content_hash == content_hash,
            PersonalizedContent.complexity_level == complexity
        ).first()
        
        if cached:
            logger.info(f"Using cached personalized content for user {user.id}, chapter {chapter_path}")
            return {
                "personalized_content": cached.personalized_content,
                "complexity_level": complexity,
                "cached": True
            }
        
        # Generate personalized content
        if settings.demo_mode:
            personalized = self._demo_personalize(content, user, complexity)
        else:
            personalized = self._ai_personalize(content, user, complexity)
        
        # Cache the result
        new_cache = PersonalizedContent(
            user_id=user.id,
            chapter_path=chapter_path,
            original_content_hash=content_hash,
            personalized_content=personalized,
            complexity_level=complexity
        )
        db.add(new_cache)
        db.commit()
        
        logger.info(f"Generated personalized content for user {user.id}, chapter {chapter_path}")
        
        return {
            "personalized_content": personalized,
            "complexity_level": complexity,
            "cached": False
        }
    
    def _demo_personalize(self, content: str, user: User, complexity: str) -> str:
        """Demo mode personalization without AI"""
        prefix = f"""
**🎯 Content Personalized for You**

**Your Profile:**
- Software Experience: {user.software_experience.title()}
- Hardware Experience: {user.hardware_experience.title()}
- Complexity Level: {complexity.title()}

---

"""
        
        if complexity == "beginner":
            prefix += "📚 *Simplified for beginners - includes extra explanations*\n\n"
        elif complexity == "expert":
            prefix += "🚀 *Advanced content - assumes prior knowledge*\n\n"
        
        return prefix + content
    
    def _ai_personalize(self, content: str, user: User, complexity: str) -> str:
        """AI-powered personalization"""
        try:
            system_prompt = f"""You are personalizing technical content for a reader with:
- Software Experience: {user.software_experience}
- Hardware Experience: {user.hardware_experience}
- Target Complexity: {complexity}
- Programming Languages: {user.programming_languages or 'Not specified'}
- Industry: {user.industry_background or 'Not specified'}
- Goals: {user.learning_goals or 'Not specified'}

Adjust the content to match their level:
- For beginners: Add more explanations, examples, and definitions
- For intermediate: Balance theory and practice
- For advanced/expert: Focus on nuances, best practices, and edge cases

Keep the same structure but adjust language and depth. Maintain markdown formatting."""
            
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Personalize this content:\n\n{content}"}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI personalization failed: {e}")
            return self._demo_personalize(content, user, complexity)


personalization_service = PersonalizationService()
