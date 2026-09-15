from app.rag.ingestion.loader import load_documents
from app.rag.ingestion.splitter import split_documents
from app.rag.ingestion.embeddings import get_embeddings
from app.rag.retrieval.vectorstore import create_vectorstore


def ingest_documents():

    # print("Loading documents...")

    documents = load_documents("data")

    # print(f"Loaded documents: {len(documents)}")

    chunks = split_documents(documents)

    # print(f"Created chunks: {len(chunks)}")

    embeddings = get_embeddings()

    # print("Embedding model created")

    vectorstore = create_vectorstore(chunks, embeddings)

    # print("Documents successfully stored in Qdrant")

    return vectorstore

# vectorstore = ingest_documents()


if __name__ == "__main__":
    ingest_documents()

