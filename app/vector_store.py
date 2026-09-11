import os
import chromadb
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from embeddings import embed_texts
from config import CHROMA_DB_DIR, COLLECTION_NAME, CHROMA_COLLECTION_METADATA, QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME

os.makedirs(CHROMA_DB_DIR, exist_ok=True)

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


# Add to ChromaDB

def add_to_chroma(chunks, embeddings=None):
    if embeddings is None:
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embed_texts(texts)

    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata=CHROMA_COLLECTION_METADATA
    )

    ids = [f"doc_{i}" for i in range(len(chunks))]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [{"source": chunk["source"]} for chunk in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")


# Add to Qdrant

def add_to_qdrant(chunks, embeddings=None):
    if embeddings is None:
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embed_texts(texts)

    points = [
        PointStruct(
            id=i,
            vector=embeddings[i],
            payload={"source": chunks[i]["source"], "text": chunks[i]["text"]}
        )
        for i in range(len(chunks))
    ]

    qdrant_client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        points=points
    )

    print(f"Stored {len(chunks)} chunks in Qdrant.")
