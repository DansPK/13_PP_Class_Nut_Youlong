import os

from dotenv import load_dotenv
load_dotenv()  # reads .env into os.environ -- must happen before any module below reads env vars

from ingest import load_documents
from chunking import chunk_text
from embeddings import embed_texts, embed_query
from vector_store import add_to_chroma, add_to_qdrant, search_chroma, search_qdrant

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 120))

docs = load_documents()
print(f"Loaded {len(docs)} documents")

# chunk every document, keeping track of which file each chunk came from
all_chunks = []
for filename, text in docs:
    for piece in chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
        all_chunks.append({"text": piece, "source": filename})

print(f"Produced {len(all_chunks)} chunks total")

# embed all chunks in one batch call
embeddings = embed_texts([c["text"] for c in all_chunks])
print(f"Embedded {len(embeddings)} chunks ({len(embeddings[0])} dims each)")

# store the same chunks + embeddings into both vector stores
add_to_chroma(all_chunks, embeddings)
add_to_qdrant(all_chunks, embeddings)
print("Stored into ChromaDB and Qdrant")

# now ask the same question against both and compare
question = "how do I reset a forgotten PIN?"
query_embedding = embed_query(question)

print(f"\n--- Query: '{question}' ---")

# print("\nChromaDB results:")
# for r in search_chroma(query_embedding, top_k=3):
#     print(f"[{r['source']}] (distance={r['distance']:.4f}) {r['text'][:100]}...")

print("\nQdrant results:")
for r in search_qdrant(query_embedding, top_k=3):
    print(f"[{r['source']}] (score={r['score']:.4f}) {r['text'][:100]}...")
