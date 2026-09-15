


from app.graph.state import RAGState
from app.rag.retrieval.prompts import format_documents, rag_prompt
from app.llm import get_llm


# ============================================================
# Retrieve documents
# ============================================================

def create_retrieve_documents_node(retriever):

    def retrieve_documents(state: RAGState):

        query = state["query"]

        documents = retriever.invoke(query)

        return {
            "documents": documents
        }

    return retrieve_documents


# ============================================================
# Grade documents
# ============================================================

def grade_documents(query, documents):

    llm = get_llm()

    relevant_documents = []

    for document in documents:

        prompt = f"""
You are a document relevance grader.

User question:
{query}

Document:
{document.page_content}

Determine whether this document contains information
that can help answer the user's question.

Return only one word:

YES
or
NO
"""

        try:

            response = llm.invoke(prompt)

            result = response.content.strip().upper()

            # Handle accidental extra text
            if result.startswith("YES"):
                relevant_documents.append(document)

        except Exception:
            continue

    return relevant_documents


# ============================================================
# Grade documents node
# ============================================================

def grade_documents_node(state: RAGState):

    documents = state.get("documents", [])

    if not documents:

        return {
            "documents": [],
            "relevance": "not_relevant",
        }

    relevant_documents = grade_documents(
        state["query"],
        documents,
    )

    if relevant_documents:

        return {
            "documents": relevant_documents,
            "relevance": "relevant",
        }

    return {
        "documents": [],
        "relevance": "not_relevant",
    }


# ============================================================
# Rewrite query
# ============================================================

def rewrite_query(state: RAGState):

    llm = get_llm()

    retry_count = state.get(
        "retry_count",
        0,
    )

    prompt = f"""
Rewrite the following user question to make it
more useful for semantic document retrieval.

Original question:
{state["query"]}

Rules:

- Preserve the original meaning.
- Make the question clear and specific.
- Do not answer the question.
- Return only the rewritten question.

Rewritten question:
"""

    response = llm.invoke(prompt)

    new_query = response.content.strip()

    return {
        "query": new_query,
        "retry_count": retry_count + 1,
    }


# ============================================================
# Decision after document grading
# ============================================================

def decide_after_grading(state: RAGState):

    if state.get("relevance") == "relevant":

        return "format_context"

    retry_count = state.get(
        "retry_count",
        0,
    )

    # Maximum 2 rewrite attempts
    if retry_count < 2:

        return "rewrite_query"

    return "no_relevant_documents"


# ============================================================
# No relevant documents
# ============================================================

def no_relevant_documents(state: RAGState):

    return {
        "answer": (
            "I could not find relevant information "
            "in the available documents."
        )
    }


# ============================================================
# Format context
# ============================================================

def format_context(state: RAGState):

    context = format_documents(
        state.get("documents", [])
    )

    return {
        "context": context
    }


# ============================================================
# Create RAG prompt
# ============================================================

def create_prompt(state: RAGState):

    history = state.get(
        "history",
        [],
    )

    history_text = ""

    if history:

        history_lines = []

        for message in history:

            role = message.get(
                "role",
                "",
            )

            content = message.get(
                "content",
                "",
            )

            if content:

                history_lines.append(
                    f"{role.upper()}: {content}"
                )

        history_text = "\n".join(
            history_lines
        )

    prompt_value = rag_prompt.invoke(
        {
            "context": state.get(
                "context",
                "",
            ),
            "input": state["query"],
            "history": history_text,
        }
    )

    return {
        "messages": prompt_value.messages
    }


# ============================================================
# Generate answer
# ============================================================

def generate_answer(state: RAGState):

    llm = get_llm()

    messages = state.get(
        "messages",
        [],
    )

    response = llm.invoke(
        messages
    )

    return {
        "answer": response.content
    }