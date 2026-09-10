"""
RAG Pipeline: Connects retriever and generator.

Takes a question, retrieves relevant chunks, and generates a grounded answer.
"""

from ingest import load_documents

docs = load_documents()

print(f"Loaded {len(docs)} documents")
for filename, text in docs:
    print(f"- {filename}: {len(text)} characters")
