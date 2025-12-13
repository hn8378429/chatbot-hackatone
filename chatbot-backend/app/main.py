# chatbot-backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from app.api import chat, auth, content
from app.models.database import init_db
from app.models.schemas import HealthResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for AI-Driven Book",
    version="1.0.0"
)

# CORS - Direct origins
origins = [
    "http://localhost:3000",   # Next.js dev server
    "http://127.0.0.1:3000",
    "http://localhost:3002",   # Docusaurus serve
    "http://127.0.0.1:3002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat.router)
app.include_router(auth.router)
app.include_router(content.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting RAG Chatbot API...")
    try:
        init_db()  # Agar DB ready nahi hai to warning show hogi
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Skipping DB init (optional): {str(e)}")
    logger.info("RAG Chatbot API started successfully")

@app.get("/", response_model=HealthResponse)
async def root():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "services": {"database": False, "vector_store": False, "openai": True}
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "services": {"database": False, "vector_store": False, "openai": True}
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "timestamp": datetime.utcnow().isoformat(), "error": str(e)}
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
