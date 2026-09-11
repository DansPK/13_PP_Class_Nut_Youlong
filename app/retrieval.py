import chromadb
from qdrant_client import QdrantClient
from embeddings import embed_query
from config import (
    TOP_K, SIMILARITY_THRESHOLD, CHROMA_DB_DIR, COLLECTION_NAME, CHROMA_COLLECTION_METADATA,
    QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME,
)

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
chroma_collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME, metadata=CHROMA_COLLECTION_METADATA)

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


#Search in ChromaDB

def search_chroma(query: str, top_k: int = TOP_K, similarity_threshold: float = SIMILARITY_THRESHOLD):
    query_embedding = embed_query(query)

    results = chroma_collection.query(query_embeddings=[query_embedding], n_results=top_k)

    matches = []
    for i in range(len(results["ids"][0])):
        similarity = 1 - results["distances"][0][i]  # cosine distance -> similarity
        if similarity >= similarity_threshold:
            matches.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "similarity": similarity
            })

    return matches


#Search in Qdrant

def search_qdrant(query: str, top_k: int = TOP_K, similarity_threshold: float = SIMILARITY_THRESHOLD):
    query_embedding = embed_query(query)

    results = qdrant_client.query_points(
        collection_name=QDRANT_COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        score_threshold=similarity_threshold
    ).points

    return [
        {"text": point.payload["text"], "source": point.payload["source"], "similarity": point.score}
        for point in results
    ]

