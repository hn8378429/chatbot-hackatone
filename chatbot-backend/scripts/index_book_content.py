"""
Script to index book content into the RAG system.
Run this after deployment to populate the vector store.
"""

import os
import sys
from pathlib import Path
import asyncio
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")


async def index_markdown_file(file_path: Path, api_url: str, docs_dir: Path):
    """Index a single markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract relative path as source
    source = str(file_path.relative_to(docs_dir))
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{api_url}/api/v1/index",
            json={
                "content": content,
                "source": source,
                "metadata": {
                    "file_type": "markdown",
                    "file_name": file_path.name
                }
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Indexed {source}: {data['chunks_indexed']} chunks")
        else:
            print(f"✗ Failed to index {source}: {response.text}")


async def index_all_docs():
    """Index all markdown files in the docs directory"""
    docs_dir = Path(__file__).parent.parent.parent / "book" / "docs"
    
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        return
    
    # Find all markdown files
    md_files = list(docs_dir.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files to index...")
    print(f"Using API: {API_URL}")
    print("-" * 60)
    
    # Index each file
    for md_file in md_files:
        await index_markdown_file(md_file, API_URL, docs_dir)
    
    print("-" * 60)
    print(f"✓ Indexing complete! Indexed {len(md_files)} files.")


if __name__ == "__main__":
    asyncio.run(index_all_docs())
