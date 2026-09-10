# RAG Pipeline - Application Structure

This folder contains the Retrieval-Augmented Generation (RAG) pipeline for a chat-with-documents application.

## Components

### 1. **ingestion.py** 📥
Loads raw documents from the documents folder. Reads PDF, TXT, DOCX, Markdown files and prepares them for processing.

### 2. **chunking.py** ✂️
Splits documents into manageable chunks. Implements text splitting strategies with configurable chunk size and overlap.

### 3. **embeddings.py** 🔢
Converts text chunks into vector embeddings. Uses a local embedding model to transform chunks into numerical representations.

### 4. **vector_store.py** 🗄️
Abstract vector database layer supporting multiple backends: pgvector, ChromaDB, Qdrant. Handles storage and similarity search.

### 5. **retrieval.py** 🔍
Finds the most relevant chunks for a question. Takes question as input, converts to embedding, and searches vector store.

### 6. **generate.py** 💡
Sends question and chunks to LLM for answer generation. Returns answer with citations.

### 7. **pipeline.py** 🔄
Connects retriever and generator into one flow. Orchestrates: Question → Retrieve → Generate → Answer

### 8. **main.py** 🚀
Main entry point. Exposes simple functions for programmatic use.

## Data Flow

```
📄 Raw Documents (documents/)
        ↓
   ingestion.py (load)
        ↓
   chunking.py (split)
        ↓
   embeddings.py (vectorize)
        ↓
   vector_store.py (save)
        ↓
   [Vector Database]
        ↓
   User Question
        ↓
   embeddings.py (vectorize)
        ↓
   retrieval.py (search)
        ↓
   generate.py (LLM)
        ↓
   Answer + Sources
```

## Configuration

See `.env-example` for all available configuration options.
