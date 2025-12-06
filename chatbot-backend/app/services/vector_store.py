from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
from typing import List, Dict, Any
import hashlib
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Handle vector storage and retrieval with Qdrant"""
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False,  # Use HTTP for Qdrant Cloud
        )
        self.collection_name = settings.qdrant_collection_name
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Ensure collection exists, create if not"""
        collections = self.client.get_collections().collections
        collection_names = [col.name for col in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small dimension
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Created collection: {self.collection_name}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI"""
        response = self.openai_client.embeddings.create(
            model=settings.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def add_documents(
        self, 
        texts: List[str], 
        metadatas: List[Dict[str, Any]]
    ) -> List[str]:
        """Add documents to vector store"""
        points = []
        chunk_ids = []
        
        for idx, (text, metadata) in enumerate(zip(texts, metadatas)):
            # Generate unique ID
            chunk_id = hashlib.md5(
                f"{metadata.get('source', '')}_{idx}_{text[:100]}".encode()
            ).hexdigest()
            
            # Generate embedding
            embedding = self.generate_embedding(text)
            
            # Create point
            point = PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    "text": text,
                    **metadata
                }
            )
            
            points.append(point)
            chunk_ids.append(chunk_id)
        
        # Upload to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        logger.info(f"Added {len(points)} documents to vector store")
        return chunk_ids
    
    def search(
        self, 
        query: str, 
        top_k: int = 5,
        filter_conditions: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        query_embedding = self.generate_embedding(query)
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=filter_conditions
        )
        
        return [
            {
                "text": hit.payload.get("text", ""),
                "score": hit.score,
                "metadata": {
                    k: v for k, v in hit.payload.items() 
                    if k != "text"
                }
            }
            for hit in results
        ]


# Global instance - initialized lazily to avoid connection errors at startup
_vector_store_instance = None

def get_vector_store() -> VectorStore:
    """Get or create vector store instance"""
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance

# For backward compatibility
vector_store = None  # Will be initialized on first use
