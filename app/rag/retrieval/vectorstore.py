
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from app.config import QDRANT_API_KEY, QDRANT_URL, QDRANT_COLLECTION_NAME
from app.rag.ingestion.embeddings import get_embeddings

def create_vectorstore(chunks, embeddings):

    vectorstore = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=QDRANT_COLLECTION_NAME,
        # force_recreate=True,
        batch_size=16
    )

    # print("Vector store created successfully!")
    
    return vectorstore


def get_vectorstore(embeddings):

    client = QdrantClient(
        url=QDRANT_URL, 
        api_key=QDRANT_API_KEY, 
        timeout=120)

    vectorstore = QdrantVectorStore(
        client=client, 
        collection_name=QDRANT_COLLECTION_NAME, 
        embedding=embeddings)

    # print("Connected to Qdrant successfully!")

    return vectorstore


# if __name__ == "__main__":
#     print("Vector store created successfully!")
