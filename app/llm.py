
from app.config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, BASE_URL
from langchain_openai import ChatOpenAI



def get_llm():

    llm = ChatOpenAI(
        model=GROQ_MODEL,
        temperature=float(GROQ_TEMPERATURE),
        api_key=GROQ_API_KEY,
        base_url=BASE_URL
    )

    return llm




