import os
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/ai_powered_lms",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "development-only-secret-change-me",
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "2"))
    )

    FRONTEND_ORIGIN = os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:5173",
    )

    # Phase 6 AI configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "pgvector")
    AI_REQUEST_TIMEOUT_SECONDS = float(
        os.getenv("AI_REQUEST_TIMEOUT_SECONDS", "30")
    )
    RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))
    RAG_MAX_COSINE_DISTANCE = float(
        os.getenv("RAG_MAX_COSINE_DISTANCE", "0.45")
    )
    RAG_CHUNK_WORDS = int(os.getenv("RAG_CHUNK_WORDS", "220"))
    RAG_CHUNK_OVERLAP_WORDS = int(
        os.getenv("RAG_CHUNK_OVERLAP_WORDS", "40")
    )
