

from typing import Annotated, TypedDict, List
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class RAGState(TypedDict, total=False):

    query: str
    history: List[dict]
    documents: List[Document]
    relevance: str
    context: str
    messages: Annotated[List[BaseMessage], add_messages]
    answer: str
    retry_count: int
 
