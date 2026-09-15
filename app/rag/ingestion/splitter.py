from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_OVERLAP, CHUNK_SIZE
# from app.rag.ingestion import load_documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

       
    return chunks



# if __name__ == "__main__":
#     documents = load_documents("data")
    
#     print(f"Number of documents: {len(documents)}")

#     chunks = split_documents(documents)

#     print(f"Total documents: {len(documents)}")
#     print(f"Total chunks created: {len(chunks)}")

#     for i, chunk in enumerate(chunks):
#             print(f"\n{'=' * 50}")
#             print(f"CHUNK {i + 1}")
#             print(f"{'=' * 50}")
#             print(chunk.page_content)
#             print(chunk.metadata)
#             print(f"\nCharacters: {len(chunk.page_content)}")

#     print(f"\nFinal chunk count: {len(chunks)}")

