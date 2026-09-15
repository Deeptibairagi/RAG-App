
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# RAG Prompt
# ============================================================

rag_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are ThinkSmarter, an intelligent document
question-answering assistant.

Your task is to answer the user's question using
the provided document context.

Rules:

1. Use the provided context as the primary source.
2. Do not invent facts that are not supported by the context.
3. If the answer is not available in the context,
   clearly say that the information is not available
   in the uploaded documents.
4. Use conversation history only to understand
   follow-up questions.
5. Give a clear and concise answer.
6. When appropriate, explain the answer using
   bullet points.
7. Do not mention internal RAG, retrieval, grading,
   or LangGraph implementation details.

Conversation history:

{history}

Document context:

{context}
""",
        ),
        (
            "human",
            "{input}",
        ),
    ]
)


# ============================================================
# Format retrieved documents
# ============================================================

def format_documents(documents):

    if not documents:

        return "No relevant documents were retrieved."

    formatted_documents = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        source = document.metadata.get(
            "source",
            "Unknown",
        )

        content = document.page_content.strip()

        formatted_documents.append(
            f"""
--- Document {index} ---
Source: {source}

{content}
"""
        )

    return "\n".join(
        formatted_documents
    )