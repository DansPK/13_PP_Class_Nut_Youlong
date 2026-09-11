"""
Run this once (or whenever documents change) to build the vector stores.
Flow: load documents -> chunk -> embed -> store in ChromaDB + Qdrant.
"""

from dotenv import load_dotenv
load_dotenv()

from ingest import load_documents
from chunking import chunk_text
from embeddings import embed_texts
from vector_store import add_to_chroma, add_to_qdrant
from config import CHUNK_SIZE, CHUNK_OVERLAP

docs = load_documents()

chunks = []
for filename, text in docs:
    for piece in chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
        chunks.append({"text": piece, "source": filename})

embeddings = embed_texts([c["text"] for c in chunks])

add_to_chroma(chunks, embeddings)
add_to_qdrant(chunks, embeddings)

print(f"Done: embedded and stored {len(chunks)} chunks from {len(docs)} documents.")
