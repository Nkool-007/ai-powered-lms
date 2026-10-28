# Merge these attributes into the existing Config class in backend/app/config.py.

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "pgvector")
AI_REQUEST_TIMEOUT_SECONDS = float(os.getenv("AI_REQUEST_TIMEOUT_SECONDS", "30"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))
RAG_MAX_COSINE_DISTANCE = float(os.getenv("RAG_MAX_COSINE_DISTANCE", "0.45"))
RAG_CHUNK_WORDS = int(os.getenv("RAG_CHUNK_WORDS", "220"))
RAG_CHUNK_OVERLAP_WORDS = int(os.getenv("RAG_CHUNK_OVERLAP_WORDS", "40"))
