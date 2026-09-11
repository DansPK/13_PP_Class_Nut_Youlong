from openai import OpenAI
from config import EMBED_MODEL, OPENAI_BASE_URL, OPENAI_COMPATIBLE_API_KEY

client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_COMPATIBLE_API_KEY,
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
