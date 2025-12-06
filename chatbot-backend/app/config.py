from pydantic_settings import BaseSettings
from typing import List


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
    
    # Qdrant
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "book_embeddings"
    
    # Neon Postgres
    database_url: str
    
    # JWT Authentication
    jwt_secret_key: str = "your-secret-key-change-in-production-min-32-chars-long-random-string"
    
    # Server
    environment: str = "development"
    cors_origins: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
