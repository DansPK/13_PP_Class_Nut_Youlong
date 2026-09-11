#Load from env


import os
from pathlib import Path


# __file__ is this file's path; parent.parent goes app/ -> project root
BASE_DIR = Path(__file__).resolve().parent.parent

# --- LLM endpoint ---
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_COMPATIBLE_API_KEY = os.getenv("OPENAI_COMPATIBLE_API_KEY", "not-needed")

# --- Models ---
EMBED_MODEL = os.getenv("EMBED_MODEL")
GEN_MODEL = os.getenv("GEN_MODEL")

# --- Storage ---
DATA_DIR = str(BASE_DIR / os.getenv("DATA_DIR", "data"))
CHROMA_DB_DIR = str(BASE_DIR / "data" / os.getenv("CHROMA_DB_DIR", "chroma_db"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")
CHROMA_HNSW_SPACE = os.getenv("CHROMA_HNSW_SPACE", "cosine")
CHROMA_COLLECTION_METADATA = {"hnsw:space": CHROMA_HNSW_SPACE}

# --- Chunking ---
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 120))

# --- Qdrant ---
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "documents")

# --- Retrieval ---
TOP_K = int(os.getenv("TOP_K", 4))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.0))

# --- Generation ---
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))
FALLBACK_MESSAGE = "I don't have enough information in the documents to answer that."

SYSTEM_PROMPT = f"""

You are a helpful assistant that answers questions using ONLY the context provided below and the prior conversation.If the answer is not contained in either, reply with EXACTLY this sentence and nothing else: "{FALLBACK_MESSAGE}" Do not add any citations, source lists, or explanation of what the sources do or don't contain when you give this reply.
Do not use outside knowledge. Otherwise, end your answer with a blank line, then cite every source you actually used as [id] filename, e.g. [01] 001_Example.txt.

"""
