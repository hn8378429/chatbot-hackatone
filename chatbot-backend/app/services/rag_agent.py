import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging
from app.config import settings
from app.services.vector_store import get_vector_store

logger = logging.getLogger(__name__)


class RAGAgent:
    """RAG-powered chatbot using Google Gemini (FREE) or OpenAI"""
    
    def __init__(self):
        self.ai_provider = settings.ai_provider
        
        if self.ai_provider == "gemini":
            # Configure Gemini (FREE TIER)
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
            logger.info(f"Initialized Gemini model: {settings.gemini_model}")
        else:
            # OpenAI fallback
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model_name = settings.openai_model
            logger.info(f"Initialized OpenAI model: {settings.openai_model}")
    
    def retrieve_context(
        self, 
        query: str, 
        selected_text: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context from vector store"""
        if selected_text:
            # If user selected text, use it as primary context
            return [{
                "text": selected_text,
                "score": 1.0,
                "metadata": {"source": "user_selection"}
            }]
        
        # Otherwise, try to search vector store
        try:
            return get_vector_store().search(query, top_k=top_k)
        except Exception as e:
            logger.warning(f"Vector store search failed: {e}. Continuing without RAG context.")
            return []
    
    def generate_response(
        self, 
        user_message: str,
        context: List[Dict[str, Any]],
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """Generate response using retrieved context"""
        
        # Demo mode - return mock response without calling any AI
        if settings.demo_mode:
            if context and context[0].get('text'):
                selected = context[0]['text'][:100]
                return f"📚 **Demo Mode Response**\n\nYou asked: '{user_message}'\n\nBased on the selected text: '{selected}...'\n\nThis is a demo response. The book discusses AI-driven development and embedded systems.\n\n✨ Enable AI (Gemini or OpenAI) in config to get real intelligent responses!"
            else:
                return f"📚 **Demo Mode Response**\n\nYou asked: '{user_message}'\n\nThis book is about AI-Driven Development and Embedded Systems! It covers spec-driven development, AI integration, and hardware programming.\n\n✨ Enable AI to get intelligent, context-aware responses!"
        
        # Build context string
        context_text = "\n\n".join([
            f"[Source: {ctx['metadata'].get('source', 'unknown')}]\n{ctx['text']}"
            for ctx in context
        ])
        
        # Build system message
        system_message = f"""You are a helpful AI assistant for an AI-Driven Book about Spec-Driven Development, AI, and Embedded Systems.

Your role is to answer questions about the book's content accurately and helpfully.

Context from the book:
{context_text}

Guidelines:
1. Answer based primarily on the provided context
2. If the context doesn't contain relevant information, say so honestly
3. Be concise but comprehensive
4. Use examples from the book when helpful
5. If user selected specific text, focus your answer on that selection
"""
        
        # Generate response based on provider
        try:
            if self.ai_provider == "gemini":
                # Use Gemini
                prompt = f"{system_message}\n\nUser: {user_message}\n\nAssistant:"
                
                # Add chat history if available
                if chat_history:
                    history_text = "\n".join([
                        f"User: {msg['user']}\nAssistant: {msg['assistant']}"
                        for msg in chat_history[-5:]
                    ])
                    prompt = f"{system_message}\n\nChat History:\n{history_text}\n\nUser: {user_message}\n\nAssistant:"
                
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        'top_p': 0.95,
                        'top_k': 40,
                        'max_output_tokens': 1000,
                    }
                )
                return response.text
            else:
                # Use OpenAI
                messages = [{"role": "system", "content": system_message}]
                
                if chat_history:
                    for msg in chat_history[-5:]:
                        messages.append({"role": "user", "content": msg["user"]})
                        messages.append({"role": "assistant", "content": msg["assistant"]})
                
                messages.append({"role": "user", "content": user_message})
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI API error: {e}")
            # Return helpful error message
            if "quota" in str(e).lower() or "429" in str(e) or "insufficient_quota" in str(e):
                return f"⚠️ **API Quota Exhausted**\n\nThe AI service has reached its usage limit. To continue:\n\n1. **Using Gemini (FREE)**: Get a free API key from https://aistudio.google.com/apikey\n2. Set `AI_PROVIDER=gemini` and `GEMINI_API_KEY=your-key` in .env\n3. Restart the backend\n\n💡 Gemini offers 15 requests/minute for free!"
            else:
                return f"⚠️ **Error**: {str(e)}\n\nPlease check your API configuration or enable demo mode."
    
    def chat(
        self, 
        user_message: str,
        selected_text: Optional[str] = None,
        chat_history: List[Dict[str, str]] = None
    ) -> tuple[str, List[Dict[str, Any]]]:
        """Main chat function - retrieve context and generate response"""
        # Retrieve relevant context
        context = self.retrieve_context(user_message, selected_text)
        
        logger.info(f"Retrieved {len(context)} context chunks for query")
        
        # Generate response
        response = self.generate_response(
            user_message, 
            context, 
            chat_history
        )
        
        return response, context


# Global instance
rag_agent = RAGAgent()
