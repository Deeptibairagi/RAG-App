

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.routes import router
# from app.database.connection import init_database


# # ============================================================
# # Initialize database
# # ============================================================

# init_database()


# # ============================================================
# # FastAPI application
# # ============================================================

# app = FastAPI(
#     title="ThinkSmarter RAG API",
#     description=(
#         "Retrieval-Augmented Generation API "
#         "powered by LangChain and LangGraph."
#     ),
#     version="1.0.0",
# )


# # ============================================================
# # CORS
# # ============================================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:8501",
#         "http://127.0.0.1:8501",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ============================================================
# # API routes
# # ============================================================

# app.include_router(
#     router
# )


# # ============================================================
# # Root endpoint
# # ============================================================

# @app.get("/")
# def root():

#     return {
#         "status": "running",
#         "service": "ThinkSmarter RAG API",
#     }


# # ============================================================
# # Health endpoint
# # ============================================================

# @app.get("/health")
# def health():

#     return {
#         "status": "healthy",
#         "service": "ThinkSmarter RAG API",
#     }




import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.database.connection import init_database


# ============================================================
# Environment
# ============================================================

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:8501",
)

# Optional additional frontend URLs
ALLOWED_ORIGINS = [
    FRONTEND_URL,
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]


# Remove duplicates while preserving order
ALLOWED_ORIGINS = list(dict.fromkeys(ALLOWED_ORIGINS))


# ============================================================
# Database initialization
# ============================================================

try:
    init_database()
except Exception as exc:
    print(f"Database initialization warning: {exc}")


# ============================================================
# FastAPI application
# ============================================================

app = FastAPI(
    title="ThinkSmarter RAG API",
    description=(
        "Production-ready Retrieval-Augmented Generation API "
        "powered by LangChain, LangGraph and Qdrant."
    ),
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API routes
# ============================================================

app.include_router(router)


# ============================================================
# Root endpoint
# ============================================================

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "ThinkSmarter RAG API",
        "environment": ENVIRONMENT,
    }


# ============================================================
# Health endpoint
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ThinkSmarter RAG API",
        "environment": ENVIRONMENT,
    }