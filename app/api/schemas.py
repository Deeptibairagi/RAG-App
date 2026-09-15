from typing import Any, List, Optional

from pydantic import BaseModel, Field


# ============================================================
# Chat message
# ============================================================

class ChatMessage(BaseModel):

    role: str

    content: str


# ============================================================
# Ask question request
# ============================================================

class AskQuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
    )

    history: List[ChatMessage] = []


# ============================================================
# Ask question response
# ============================================================

class AskQuestionResponse(BaseModel):

    success: bool

    answer: str = ""

    error: str = ""

    details: Optional[Any] = None