#!/usr/bin/env python3
"""Test Qdrant connection"""
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

print(f"Testing Qdrant connection...")
print(f"URL: {qdrant_url}")
print(f"API Key: {qdrant_api_key[:20]}...")

try:
    # Try with prefer_grpc=False
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=False,
    )
    collections = client.get_collections()
    print(f"\n✓ Successfully connected to Qdrant!")
    print(f"Collections: {collections}")
except Exception as e:
    print(f"\n✗ Failed to connect:")
    print(f"Error: {e}")
    print("\nTrying alternative approaches...")
    
    # Try without https://
    try:
        alt_url = qdrant_url.replace("https://", "")
        client = QdrantClient(
            host=alt_url.split(":")[0],
            api_key=qdrant_api_key,
            prefer_grpc=False,
            https=True,
        )
        collections = client.get_collections()
        print(f"✓ Connected with alternative method!")
        print(f"Collections: {collections}")
    except Exception as e2:
        print(f"✗ Alternative also failed: {e2}")
