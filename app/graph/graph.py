from functools import lru_cache

from langgraph.graph import StateGraph

from app.graph.state import RAGState
from app.graph.nodes import (
    create_retrieve_documents_node,
    no_relevant_documents,
    grade_documents_node,
    rewrite_query,
    format_context,
    create_prompt,
    generate_answer,
)
from app.graph.edges import add_edges

from app.rag.ingestion.embeddings import get_embeddings
from app.rag.retrieval.vectorstore import get_vectorstore
from app.rag.retrieval.retriever_reranking import get_retriever



@lru_cache(maxsize=1)
def build_graph():

     # Load embeddings only when graph is first used

    embeddings = get_embeddings()


    # ========================================================
    # Vector store
    # ========================================================

    vectorstore = get_vectorstore(embeddings)

    # ========================================================
    # Retriever
    # ========================================================

    retriever = get_retriever(vectorstore)

    # ========================================================
    # State graph
    # ========================================================

    graph_builder = StateGraph(RAGState)

    # ========================================================
    # Nodes
    # ========================================================

    retrieve_documents_node = (create_retrieve_documents_node(retriever))

    graph_builder.add_node("retrieve_documents", retrieve_documents_node)

    graph_builder.add_node("grade_documents", grade_documents_node)

    graph_builder.add_node("rewrite_query", rewrite_query)

    graph_builder.add_node("format_context", format_context)

    graph_builder.add_node("create_prompt", create_prompt)

    graph_builder.add_node("generate_answer", generate_answer)

    graph_builder.add_node("no_relevant_documents", no_relevant_documents)

    # ========================================================
    # Edges
    # ========================================================

    add_edges(graph_builder)

    # ========================================================
    # Compile
    # ========================================================

    graph = graph_builder.compile()

    return graph