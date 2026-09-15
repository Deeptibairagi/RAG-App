# import os
# from dotenv import load_dotenv

# from pathlib import Path

# load_dotenv()


# MODEL = os.getenv("MODEL")


# # LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
# # HUGGINGFACEHUB_API_TOKEN=os.getenv("HUGGINGFACEHUB_API_TOKEN")

# QDRANT_URL = os.getenv("QDRANT_URL")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# QDRANT_COLLECTION_NAME  = os.getenv("QDRANT_COLLECTION_NAME")

# EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# RERANKER_MODEL_NAME = os.getenv("RERANKER_MODEL_NAME")

# CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
# CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))

# TOP_K = int(os.getenv("TOP_K"))
# TOP_n = int(os.getenv("TOP_n"))
# # threshold = float(os.getenv("threshold"))

# API_URL= os.getenv("API_URL")


# DATABASE_PATH = os.getenv("DATABASE_PATH")


# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = os.getenv("GROQ_MODEL")
# GROQ_TEMPERATURE = os.getenv("GROQ_TEMPERATURE")
# BASE_URL = os.getenv("BASE_URL")


# ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")




import os
from pathlib import Path

from dotenv import load_dotenv


# ============================================================
# Load local .env
# ============================================================

load_dotenv()


# ============================================================
# Helper
# ============================================================

def get_env(
    name: str,
    default=None,
    required: bool = False,
):
    """
    Read configuration from environment variables.

    For Streamlit Cloud, values can also be supplied through
    Streamlit secrets because Streamlit exposes secrets to the
    application environment.
    """

    value = os.getenv(name)

    if value is None or value == "":
        value = default

    if required and (value is None or value == ""):
        raise RuntimeError(
            f"Required environment variable '{name}' is missing."
        )

    return value


def get_int(
    name: str,
    default: int,
) -> int:

    value = get_env(name, default)

    try:
        return int(value)

    except (TypeError, ValueError) as exc:
        raise RuntimeError(
            f"{name} must be an integer. "
            f"Received: {value}"
        ) from exc


def get_float(
    name: str,
    default: float,
) -> float:

    value = get_env(name, default)

    try:
        return float(value)

    except (TypeError, ValueError) as exc:
        raise RuntimeError(
            f"{name} must be a number. "
            f"Received: {value}"
        ) from exc


# ============================================================
# Application
# ============================================================

ENVIRONMENT = get_env(
    "ENVIRONMENT",
    "development",
)


# ============================================================
# API
# ============================================================

API_URL = get_env(
    "API_URL",
    "http://127.0.0.1:8000",
)


# ============================================================
# Qdrant
# ============================================================

QDRANT_URL = get_env(
    "QDRANT_URL",
    required=True,
)

QDRANT_API_KEY = get_env(
    "QDRANT_API_KEY",
    required=True,
)

QDRANT_COLLECTION_NAME = get_env(
    "QDRANT_COLLECTION_NAME",
    "thinksmarter",
)


# ============================================================
# Embeddings
# ============================================================

EMBEDDING_MODEL = get_env(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)


# ============================================================
# Reranker
# ============================================================

RERANKER_MODEL_NAME = get_env(
    "RERANKER_MODEL_NAME",
    "",
)


# ============================================================
# RAG configuration
# ============================================================

CHUNK_SIZE = get_int(
    "CHUNK_SIZE",
    1000,
)

CHUNK_OVERLAP = get_int(
    "CHUNK_OVERLAP",
    200,
)

TOP_K = get_int(
    "TOP_K",
    5,
)

TOP_n = get_int(
    "TOP_n",
    3,
)


# ============================================================
# Database
# ============================================================

DATABASE_PATH = get_env(
    "DATABASE_PATH",
    "./data/chat_history.db",
)


# ============================================================
# LLM / Groq
# ============================================================

GROQ_API_KEY = get_env(
    "GROQ_API_KEY",
    required=True,
)

GROQ_MODEL = get_env(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

GROQ_TEMPERATURE = get_float(
    "GROQ_TEMPERATURE",
    0.0,
)

# Your llm.py uses ChatOpenAI with Groq's OpenAI-compatible API.
BASE_URL = get_env(
    "BASE_URL",
    "https://api.groq.com/openai/v1",
)

# Backward compatibility with your current llm.py
base_url = BASE_URL


# ============================================================
# Application paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)