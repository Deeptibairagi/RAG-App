from qdrant_client import QdrantClient

from app.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
)


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=120,
)


collections = client.get_collections()

print("Connected to Qdrant successfully!")

print("Collections:")

for collection in collections.collections:
    print("-", collection.name)
