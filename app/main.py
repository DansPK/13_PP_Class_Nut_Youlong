"""
The whole app, end to end, exposed as plain Python functions.
No framework magic, just plain functions wired together.
"""
import logging

logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

from app.generate import generate_answer
from app.ingest import build_index
from app.retrieval import retrieve


def ingest() -> dict:
    """
    (Re)build the vector index from everything in data/.

    Returns:
        Dictionary with chunks_indexed count
    """
    pass


def chat(question: str, top_k: int | None = None) -> dict:
    """
    The full retrieve -> augment -> generate loop for one question.

    Args:
        question: The user's question
        top_k: Number of chunks to retrieve

    Returns:
        Dictionary with answer and sources
    """
    pass
