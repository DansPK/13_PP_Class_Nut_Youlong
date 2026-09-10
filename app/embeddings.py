"""
Turn text into vectors using an embedding model.

Both ingestion (embedding chunks) and retrieval (embedding the user's question)
call this, so they use the same model and never drift apart.
"""
import os
from openai import OpenAI

EMBED_MODEL = os.getenv("EMBED_MODEL")


client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_COMPATIBLE_API_KEY", "not-needed"),
)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of strings. Returns one vector per input string, same order."""
    if not texts:
        return []
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]


def embed_query(text: str) -> list[float]:
    """wrapper for embedding a single piece of text (e.g. a question)."""
    return embed_texts([text])[0]
