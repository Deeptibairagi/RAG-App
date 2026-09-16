

from fastapi import APIRouter

from app.api.schemas import AskQuestionRequest, AskQuestionResponse

import traceback

router = APIRouter(
    prefix="/api",
    tags=["Chat"],
)


# ============================================================
# Ask question
# ============================================================

@router.post(
    "/chat/ask",
    response_model=AskQuestionResponse,
)

def ask_question(request: AskQuestionRequest):

    try:

        # ----------------------------------------------------
        # Import LangGraph only when a question is asked
        # ----------------------------------------------------
    
        from app.graph.graph import build_graph

        # ----------------------------------------------------
        # Build / retrieve compiled graph
        # ----------------------------------------------------
        
        graph = build_graph()

        # ----------------------------------------------------
        # Convert history into dictionaries
        # ----------------------------------------------------

        history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.history
        ]

        # ----------------------------------------------------
        # Initial LangGraph state
        # ----------------------------------------------------

        initial_state = {
            "query": request.question,
            "history": history,
            "retry_count": 0,
        }

        # ----------------------------------------------------
        # Execute RAG pipeline
        # ----------------------------------------------------

        result = graph.invoke(initial_state)

        # ----------------------------------------------------
        # Get final answer
        # ----------------------------------------------------

        answer = result.get("answer", "")

        if not answer:

            answer = (
                "I could not generate an answer "
                "from the available documents."
            )

        return AskQuestionResponse(
            success=True,
            answer=answer,
        )

    except Exception as exc:

        print("========== RAG ERROR ==========")
        print(repr(exc))
        traceback.print_exc()
        print("================================")

        return AskQuestionResponse(
            success=False,
            answer="",
            error="Failed to process the question.",
            details=str(exc),
        )


@router.get("/chat/test")
def chat_test():
    return {
        "status": "ok",
        "message": "Latest routes.py is running",
        "request_model": "AskQuestionRequest",
    }