

from langgraph.graph import END, START

from app.graph.nodes import decide_after_grading


def add_edges(graph_builder):

    graph_builder.add_edge(START, "retrieve_documents")

    graph_builder.add_edge("retrieve_documents", "grade_documents")

    graph_builder.add_conditional_edges(
        "grade_documents",
        decide_after_grading,
        {
            "format_context": "format_context",
            "rewrite_query": "rewrite_query",
            "no_relevant_documents": "no_relevant_documents",
        },
    )

    graph_builder.add_edge("rewrite_query", "retrieve_documents")

    graph_builder.add_edge("format_context", "create_prompt")

    graph_builder.add_edge("create_prompt", "generate_answer")

    graph_builder.add_edge("generate_answer", END)

    graph_builder.add_edge("no_relevant_documents", END)

    return graph_builder