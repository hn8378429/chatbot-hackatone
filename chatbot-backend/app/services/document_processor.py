from typing import List, Dict, Any
import re
import tiktoken


class DocumentProcessor:
    """Process and chunk documents for RAG"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\'\"]+', '', text)
        return text.strip()
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        # Tokenize
        tokens = self.encoding.encode(text)
        chunks = []
        
        start = 0
        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            # Move start pointer with overlap
            start = end - self.chunk_overlap
            
            if start >= len(tokens):
                break
        
        return chunks
    
    def process_document(
        self, 
        content: str, 
        source: str, 
        metadata: Dict[str, Any] = None
    ) -> tuple[List[str], List[Dict[str, Any]]]:
        """Process document and return chunks with metadata"""
        cleaned_text = self.clean_text(content)
        chunks = self.chunk_text(cleaned_text)
        
        # Add metadata to each chunk
        metadatas = []
        for idx, chunk in enumerate(chunks):
            chunk_metadata = {
                "source": source,
                "chunk_index": idx,
                "total_chunks": len(chunks),
                **(metadata or {})
            }
            metadatas.append(chunk_metadata)
        
        return chunks, metadatas


# Global instance
doc_processor = DocumentProcessor()
