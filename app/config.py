"""
Configuration loaded from environment variables.

All other configuration is loaded from .env file. See .env-example for available options.
TOP_K and SYSTEM_PROMPT stay here as they're less likely to change per environment.
"""
import os

# --- Retrieval ---
TOP_K = int(os.getenv("TOP_K", 4))

# --- Generation ---
SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions using ONLY the "
    "context provided below. If the answer is not contained in the context, "
    "say \"I don't have enough information in the documents to answer that.\" "
    "Do not use outside knowledge. Cite the source file name(s) you used."
)
