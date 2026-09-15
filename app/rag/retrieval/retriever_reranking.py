

from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from app.config import RERANKER_MODEL_NAME, TOP_K, TOP_n



def get_retriever(vectorstore):

   
    # Step 1: Retrieve initial candidates from Qdrant
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    # print(f"Loading reranker: {RERANKER_MODEL_NAME}")


    
    # Step 2: Load cross-encoder reranker
    reranker_model = HuggingFaceCrossEncoder(model_name=RERANKER_MODEL_NAME)
    # print("Reranker loaded!")



    # Step 3: Configure reranker
    reranker = CrossEncoderReranker(model=reranker_model, top_n = TOP_n)
    # print("CrossEncoderReranker created!")


    

    # Step 4: Combine retriever + reranker
    retriever = ContextualCompressionRetriever(base_compressor=reranker, base_retriever=base_retriever)
    # print("ContextualCompressionRetriever created!")


    return retriever


# def get_documents_with_scores(vectorstore, query, k=TOP_K, threshold=threshold):
#     """
#     Performs direct vector search against Qdrant and returns
#     documents together with their vector similarity/distance scores.

#     Note:
#         The meaning of the score depends on the Qdrant distance metric.
#         For example, with distance-based metrics, lower values can mean
#         greater similarity.
#     """

#     docs_with_scores = vectorstore.similarity_search_with_score(query, k=k)

#     for doc, score in docs_with_scores:
#         print("SCORE:", score)
#         print("TEXT:", doc.page_content[:200])
#         print("-" * 50)

#     relevant_docs = [
#         doc
#         for doc, score in docs_with_scores
#         if score < threshold
#     ]

    
#     return relevant_docs



# if __name__ == "__main__":
#     print("Retriever module OK")

