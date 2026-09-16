

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

# def ask_question(request: AskQuestionRequest):

#     try:

#         # ----------------------------------------------------
#         # Import LangGraph only when a question is asked
#         # ----------------------------------------------------
    
#         from app.graph.graph import build_graph

#         # ----------------------------------------------------
#         # Build / retrieve compiled graph
#         # ----------------------------------------------------
        
#         graph = build_graph()

#         # ----------------------------------------------------
#         # Convert history into dictionaries
#         # ----------------------------------------------------

#         history = [
#             {
#                 "role": message.role,
#                 "content": message.content,
#             }
#             for message in request.history
#         ]

#         # ----------------------------------------------------
#         # Initial LangGraph state
#         # ----------------------------------------------------

#         initial_state = {
#             "query": request.question,
#             "history": history,
#             "retry_count": 0,
#         }

#         # ----------------------------------------------------
#         # Execute RAG pipeline
#         # ----------------------------------------------------

#         result = graph.invoke(initial_state)

#         # ----------------------------------------------------
#         # Get final answer
#         # ----------------------------------------------------

#         answer = result.get("answer", "")

#         if not answer:

#             answer = (
#                 "I could not generate an answer "
#                 "from the available documents."
#             )

#         return AskQuestionResponse(
#             success=True,
#             answer=answer,
#         )

#     except Exception as exc:

#         print("========== RAG ERROR ==========")
#         print(repr(exc))
#         traceback.print_exc()
#         print("================================")

#         return AskQuestionResponse(
#             success=False,
#             answer="",
#             error="Failed to process the question.",
#             details=str(exc),
#         )


def ask_question(request):

    try:
        print("========== CHAT REQUEST ==========")
        print("1. Request received")

        from app.graph.graph import build_graph

        print("2. Imported build_graph")

        graph = build_graph()

        print("3. Graph built")

        history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.history
        ]

        initial_state = {
            "query": request.question,
            "history": history,
            "retry_count": 0,
        }

        print("4. Invoking graph")

        result = graph.invoke(initial_state)

        print("5. Graph completed")

        answer = result.get("answer", "")

        if not answer:
            answer = "I could not generate an answer from the available documents."

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