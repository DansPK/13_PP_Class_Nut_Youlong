"""
Simple CLI chat app for the RAG pipeline.
Type a question, get an answer. Type 'exit' to quit.
"""

from pipeline import ask
from retrieval import search_chroma
from config import TOP_K, SIMILARITY_THRESHOLD

print("RAG Chat - ask a question (type 'exit' to quit)")

history = []

while True:
    question = input("\nYou: ")

    if question.lower() in ("exit", "quit"):
        break

    chunks = search_chroma(question, top_k=TOP_K, similarity_threshold=SIMILARITY_THRESHOLD)

    print("\nRetrieved:")
    for i, chunk in enumerate(chunks, start=1):
        preview = chunk["text"][:80].replace("\n", " ").strip()
        print(f"  [Chunk {i:02d}] ({chunk['similarity']:.2f}) {chunk['source']}: {preview}...")

    print("\nBot: ", end="")
    answer, history, chunks = ask(question, history=history, stream=True, chunks=chunks)

    print("-" * 40)
