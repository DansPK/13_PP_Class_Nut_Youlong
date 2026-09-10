"""
Store chunk embeddings in a vector database, and search them later.

For this demo we write to two vector stores side by side: ChromaDB (local,
persistent on disk) and Qdrant (running as a server). Same chunks, same
embeddings, just so we can compare the two.
"""
import os

import chromadb
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "data/chromadb")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")


# ---------- ChromaDB ----------

def get_chroma_collection():
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def add_to_chroma(chunks: list[dict], embeddings: list[list[float]]) -> None:
    """chunks is a list of {"text": ..., "source": ...} dicts, same order as embeddings."""
    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"{chunk['source']}::{i}")
        documents.append(chunk["text"])
        metadatas.append({"source": chunk["source"]})

    collection = get_chroma_collection()
    collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)


def search_chroma(query_embedding: list[float], top_k: int = 4) -> list[dict]:
    collection = get_chroma_collection()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    matches = []
    for doc, meta, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        matches.append({"text": doc, "source": meta["source"], "distance": distance})

    return matches


# ---------- Qdrant ----------

def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL)


def ensure_qdrant_collection(vector_size: int) -> None:
    """Qdrant needs the collection created upfront with a fixed vector size."""
    client = get_qdrant_client()
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


def add_to_qdrant(chunks: list[dict], embeddings: list[list[float]]) -> None:
    """chunks is a list of {"text": ..., "source": ...} dicts, same order as embeddings."""
    ensure_qdrant_collection(vector_size=len(embeddings[0]))

    points = []
    for i, chunk in enumerate(chunks):
        payload = {"text": chunk["text"], "source": chunk["source"]}
        points.append(PointStruct(id=i, vector=embeddings[i], payload=payload))

    client = get_qdrant_client()
    client.upsert(collection_name=COLLECTION_NAME, points=points)


def search_qdrant(query_embedding: list[float], top_k: int = 4) -> list[dict]:
    client = get_qdrant_client()
    results = client.query_points(
        collection_name=COLLECTION_NAME, query=query_embedding, limit=top_k
    ).points

    matches = []
    for r in results:
        matches.append({"text": r.payload["text"], "source": r.payload["source"], "score": r.score})

    return matches
