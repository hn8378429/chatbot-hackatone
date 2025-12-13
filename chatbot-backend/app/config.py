from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # AI Model Settings
    ai_provider: str = "gemini"  # "openai" or "gemini"
    
    # OpenAI (optional, if ai_provider = "openai")
    openai_api_key: str = "not-used"
    openai_model: str = "gpt-4o-mini"
    
    # Google Gemini (FREE TIER - 15 RPM, 1M TPM, 1500 RPD)
    gemini_api_key: str = ""  # Get free key from https://aistudio.google.com/apikey
    gemini_model: str = "gemini-1.5-flash-latest"  # Free tier model
    
    # Embeddings
    embedding_model: str = "text-embedding-3-small"
    demo_mode: bool = False  # Set to True to use mock responses without AI
    
    # Qdrant - Made optional for demo mode
    qdrant_url: Optional[str] = "http://localhost:6333"
    qdrant_api_key: Optional[str] = "demo_key"
    qdrant_collection_name: str = "book_embeddings"
    
    # Database - Made optional with default SQLite
    database_url: str = "sqlite:///./book_chat.db"
    
    # JWT Authentication
    jwt_secret_key: str = "your-secret-key-change-in-production-min-32-chars-long-random-string"
    
    # Server
    environment: str = "development"
    cors_origins: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignores extra fields in .env
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Create settings instance with error handling
try:
    settings = Settings()
    print(f"✅ Settings loaded successfully. Demo Mode: {settings.demo_mode}")
except Exception as e:
    print(f"⚠️ Error loading settings: {e}. Using fallback demo settings...")
    
    # Fallback demo settings
    class DemoSettings:
        ai_provider = "gemini"
        demo_mode = True
        gemini_api_key = "demo_key"
        gemini_model = "gemini-1.5-flash-latest"
        openai_api_key = "not-used"
        openai_model = "gpt-4o-mini"
        embedding_model = "text-embedding-3-small"
        qdrant_url = "http://localhost:6333"
        qdrant_api_key = "demo_key"
        qdrant_collection_name = "book_embeddings"
        database_url = "sqlite:///./book_chat.db"
        jwt_secret_key = "demo-secret-key-1234567890"
        environment = "development"
        cors_origins = "http://localhost:3000"
        
        @property
        def cors_origins_list(self):
            return ["http://localhost:3000"]
    
    settings = DemoSettings()
    print("✅ Using demo settings for hackathon")