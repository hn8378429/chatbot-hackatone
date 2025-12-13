import logging
import random
from typing import List, Dict, Any, Optional

import google.generativeai as genai

from app.config import settings
from app.services.vector_store import get_vector_store

logger = logging.getLogger(__name__)


class RAGAgent:
    """RAG-powered chatbot using Google Gemini (FREE) or OpenAI"""

    def __init__(self):
        self.ai_provider = settings.ai_provider
        self.model = None
        self.client = None
        self.model_name = None

        # ✅ IMPORTANT: DEMO MODE — SKIP AI INIT COMPLETELY
        if settings.demo_mode:
            logger.info("✅ DEMO_MODE enabled — skipping AI initialization")
            return

        # ✅ REAL AI MODE
        if self.ai_provider == "gemini":
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
            logger.info(f"Initialized Gemini model: {settings.gemini_model}")

        else:
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model_name = settings.openai_model
            logger.info(f"Initialized OpenAI model: {settings.openai_model}")

    # --------------------------------------------------

    def retrieve_context(
        self,
        query: str,
        selected_text: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context from vector store"""

        if selected_text:
            return [{
                "text": selected_text,
                "score": 1.0,
                "metadata": {"source": "user_selection"}
            }]

        try:
            return get_vector_store().search(query, top_k=top_k)
        except Exception as e:
            logger.warning(f"Vector store search failed: {e}")
            return []

    # --------------------------------------------------

    def generate_response(
        self,
        user_message: str,
        context: List[Dict[str, Any]],
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """Generate response with SMART demo mode"""

        # ✅ SMART DEMO MODE RESPONSES (NO API CALL)
        if settings.demo_mode:
            # Extract context text for analysis
            context_text = ""
            if context and context[0].get("text"):
                context_text = " ".join([c['text'][:200] for c in context[:2]])
            
            # Prepare keywords analysis
            all_keywords = [
                "AI", "artificial intelligence", "development", "software", 
                "specification", "design", "embedded", "system", "hardware",
                "code", "programming", "architecture", "model", "testing",
                "deployment", "maintenance", "framework", "API", "interface",
                "algorithm", "data", "database", "cloud", "security", "IoT"
            ]
            
            # Find keywords in context
            found_keywords = []
            if context_text:
                context_lower = context_text.lower()
                found_keywords = [k for k in all_keywords if k.lower() in context_lower]
            
            # Smart question-based responses
            question_lower = user_message.lower().strip()
            
            # GREETINGS
            if any(word in question_lower for word in ["hello", "hi", "hey", "namaste", "hola"]):
                greetings = [
                    "📚 **Book Assistant (Demo Mode)**\n\nHello! 👋 I'm your AI book assistant. In real AI mode, I would help you understand concepts from 'AI-Driven Development and Embedded Systems'.",
                    "📚 **Demo Mode**\n\nHi there! I'm ready to help you explore the book's content. Enable real AI for intelligent conversations.",
                    "📚 **Smart Demo**\n\nWelcome! This book covers cutting-edge topics in software engineering. What would you like to learn about?"
                ]
                return random.choice(greetings)
            
            # AI-RELATED QUESTIONS
            elif any(word in question_lower for word in ["ai", "artificial intelligence", "machine learning", "ml"]):
                responses = [
                    f"📚 **AI-Driven Development (Demo)**\n\n**Your Question:** {user_message}\n\n**Topic:** Artificial Intelligence\n\n**Demo Insight:** This book explores how AI transforms software development—from automated code generation to intelligent testing. Real AI would analyze specific chapters to give you detailed examples.\n\n💡 *Enable Gemini/OpenAI for deep AI analysis*",
                    f"📚 **Demo Mode - AI Focus**\n\n**Question:** {user_message}\n\n**Relevant Context:** {context_text[:150]}...\n\n**Key Points:**\n• AI-assisted coding\n• Machine learning integration\n• Intelligent debugging\n• Automated documentation\n\n🔍 *Real AI could extract exact book passages*"
                ]
                return random.choice(responses)
            
            # SPECIFICATION/DESIGN QUESTIONS
            elif any(word in question_lower for word in ["spec", "specification", "design", "architecture"]):
                responses = [
                    f"📚 **Spec-Driven Design (Demo)**\n\n**Your Question:** {user_message}\n\n**Topic:** Specification-Based Development\n\n**Demo Insight:** The book emphasizes starting with precise specifications to reduce errors. Real AI would show you exact methodologies and case studies.\n\n📖 *Chapter 3 covers this in detail*",
                    f"📚 **Demo Mode - Design Focus**\n\n**Question:** {user_message}\n\n**Design Principles Covered:**\n• Formal specifications\n• Model-driven development\n• Architecture patterns\n• Verification techniques\n\n🎯 *Enable AI for practical examples*"
                ]
                return random.choice(responses)
            
            # EMBEDDED SYSTEMS
            elif any(word in question_lower for word in ["embedded", "hardware", "iot", "raspberry", "arduino", "microcontroller"]):
                responses = [
                    f"📚 **Embedded Systems (Demo)**\n\n**Your Question:** {user_message}\n\n**Topic:** Hardware-Software Integration\n\n**Demo Insight:** This book bridges AI software with embedded hardware. Real AI would explain real-time constraints, memory management, and hardware interfaces.\n\n⚙️ *See Chapter 7 for hardware integration*",
                    f"📚 **Demo Mode - Embedded Focus**\n\n**Question:** {user_message}\n\n**Key Areas:**\n• Real-time operating systems\n• Low-power optimization\n• Sensor integration\n• Edge AI deployment\n\n🔌 *Real AI could provide code snippets*"
                ]
                return random.choice(responses)
            
            # CODE/EXAMPLES
            elif any(word in question_lower for word in ["code", "example", "program", "snippet", "function", "class"]):
                responses = [
                    f"📚 **Code Examples (Demo)**\n\n**Your Question:** {user_message}\n\n**Demo Response:** The book contains practical code examples in Python/C++. Real AI would extract and explain relevant code with line-by-line analysis.\n\n```python\n# Example structure from the book\ndef ai_assisted_function():\n    # AI-generated code\n    # Human refinement\n    # Automated testing\n    pass\n```\n💻 *Enable AI for actual code extraction*",
                    f"📚 **Demo Mode - Programming**\n\n**Question:** {user_message}\n\n**Programming Topics:**\n• AI code generation\n• Embedded C/Python\n• API design\n• Testing frameworks\n\n📝 *Real AI would show book examples*"
                ]
                return random.choice(responses)
            
            # HOW/WHY QUESTIONS
            elif question_lower.startswith(("how ", "why ", "what is ", "what are ")):
                if context_text:
                    return f"""📚 **Demo Mode - Analytical Response**

**Your Question:** {user_message}

**Relevant Context Found:** {context_text[:200]}...

**Analysis Approach:**
1. Identify key concepts in question
2. Search book passages
3. Synthesize information
4. Provide step-by-step explanation

**Detected Keywords:** {', '.join(found_keywords[:5]) if found_keywords else 'Technical concepts'}

💡 *Real AI would give a comprehensive answer using {len(context)} relevant passages*"""
                else:
                    topics = ["AI development lifecycle", "Specification techniques", "Hardware-software codesign", "Testing methodologies"]
                    return f"""📚 **Demo Mode - Question Analysis**

**Question:** {user_message}

**This appears to be about:** {random.choice(topics)}

**What the book covers:**
• Theoretical foundations
• Practical implementation
• Case studies
• Best practices

🔍 *Enable AI for precise book-based answers*"""
            
            # GENERAL QUESTIONS WITH CONTEXT
            elif context_text:
                return f"""📚 **Context-Aware Demo**

**Question:** {user_message}

**Found in Book Context:** {context_text[:180]}...

**Topics Identified:** {', '.join(found_keywords[:4]) if found_keywords else 'Relevant technical content'}

**Real AI Capabilities:**
✓ Answer based on exact book passages
✓ Provide citations and page numbers
✓ Explain complex concepts simply
✓ Connect related topics

📖 *Enable AI to access full book knowledge*"""
            
            # DEFAULT SMART RESPONSES
            else:
                smart_responses = [
                    f"📚 **Book Assistant Demo**\n\n**Question:** {user_message}\n\nI can help you explore topics from 'AI-Driven Development and Embedded Systems'. The book covers:\n\n• **AI-Assisted Programming**\n• **Formal Specification Methods**\n• **Embedded System Design**\n• **Real-World Case Studies**\n\nTry asking about specific chapters or concepts!",
                    f"📚 **Smart Demo Mode**\n\n**Your Query:** {user_message}\n\nThis book addresses modern software engineering challenges. Interesting sections include:\n\n1. **Chapter 2:** AI Tools for Developers\n2. **Chapter 4:** Specification Languages\n3. **Chapter 6:** Embedded AI Applications\n4. **Chapter 8:** Future Trends\n\nWhat interests you most?",
                    f"📚 **Demo Assistant**\n\n**Question:** {user_message}\n\n**Book Scope:** Bridging AI software with embedded hardware systems.\n\n**Key Innovations Covered:**\n• Automated code generation\n• Hardware-aware AI models\n• Cross-platform development\n• Energy-efficient algorithms\n\n🚀 *Enable real AI for detailed exploration*"
                ]
                return random.choice(smart_responses)

        # --------------------------------------------------
        # REAL AI MODE BELOW (Gemini/OpenAI)
        # --------------------------------------------------

        context_text = "\n\n".join(
            f"[Source: {c['metadata'].get('source', 'unknown')}]\n{c['text']}"
            for c in context
        )

        system_message = f"""
You are a helpful AI assistant for an AI-Driven Book titled "AI-Driven Development and Embedded Systems".

Context from the book:
{context_text}

Instructions:
1. Answer primarily using the provided context
2. Be concise but thorough
3. If information is missing from context, acknowledge it
4. Use bullet points for clarity when appropriate
5. Maintain a helpful, academic tone
"""

        try:
            if self.ai_provider == "gemini":
                prompt = f"{system_message}\n\nUser Question: {user_message}\nAssistant:"

                if chat_history:
                    history = "\n".join(
                        f"User: {h['user']}\nAssistant: {h['assistant']}"
                        for h in chat_history[-5:]
                    )
                    prompt = f"{system_message}\n\nPrevious Conversation:\n{history}\n\nUser Question: {user_message}\nAssistant:"

                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 800,
                    },
                )
                return response.text

            else:
                messages = [{"role": "system", "content": system_message}]

                if chat_history:
                    for h in chat_history[-5:]:
                        messages.append({"role": "user", "content": h["user"]})
                        messages.append({"role": "assistant", "content": h["assistant"]})

                messages.append({"role": "user", "content": user_message})

                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=800,
                )
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"AI API error: {e}")
            return (
                "⚠️ **AI Service Error**\n\n"
                "I encountered an issue connecting to the AI service. This could be due to:\n\n"
                "1. API key configuration\n"
                "2. Network connectivity\n"
                "3. Service limitations\n\n"
                "Please check your settings or enable DEMO_MODE for testing."
            )

    # --------------------------------------------------

    def chat(
        self,
        user_message: str,
        selected_text: Optional[str] = None,
        chat_history: List[Dict[str, str]] = None
    ) -> tuple[str, List[Dict[str, Any]]]:
        """Main chat entry point"""

        context = self.retrieve_context(user_message, selected_text)
        response = self.generate_response(user_message, context, chat_history)
        return response, context


# ✅ GLOBAL INSTANCE
rag_agent = RAGAgent()