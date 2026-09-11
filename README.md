# 13_PP_Class_Nut_Youlong

A small Retrieval-Augmented Generation (RAG) pipeline: it ingests `.txt` documents, chunks and embeds them, stores the vectors in ChromaDB and/or Qdrant, and answers questions over them using an OpenAI-compatible chat model.

## Setup

**Requirements:** Python >= 3.12, [uv](https://docs.astral.sh/uv/) (or pip), Docker (for Qdrant).

1. **Install dependencies**

   ```bash
   uv sync
   ```

   or, without uv:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**

   Copy `.env-example` to `.env` and fill in your values:

   ```bash
   cp .env-example .env
   ```

   | Variable | Purpose |
   |---|---|
   | `EMBED_MODEL` | Embedding model name (e.g. `nomic-embed-text`) |
   | `GEN_MODEL` | Chat/generation model name (e.g. `llama3:8b`) |
   | `OPENAI_BASE_URL` | Base URL of an OpenAI-compatible endpoint (Ollama, LM Studio, vLLM, Azure OpenAI, OpenAI itself, etc.) |
   | `OPENAI_COMPATIBLE_API_KEY` | API key for that endpoint (`not-needed` for most local servers) |
   | `DATA_DIR` | Folder of source `.txt` documents (default `data`) |
   | `CHROMA_DB_DIR` / `COLLECTION_NAME` | ChromaDB persistence path and collection name |
   | `QDRANT_URL` / `QDRANT_API_KEY` / `QDRANT_COLLECTION_NAME` | Qdrant connection details |
   | `CHUNK_SIZE` / `CHUNK_OVERLAP` | Chunking parameters, in characters |
   | `TOP_K` | Number of chunks retrieved per question (default `4`) |
   | `SIMILARITY_THRESHOLD` | Minimum cosine similarity a chunk must meet to be kept (default `0.0`; sample docs work well around `0.55`) |
   | `TEMPERATURE` | Sampling temperature for the chat model — lower is more deterministic/grounded (default `0.2`) |


3. **Start the vector store**

   Qdrant runs via Docker Compose:

   ```bash
   docker compose -f docker_services/qdrant/docker-compose.yaml up -d
   ```

   ChromaDB needs no separate service — it's an embedded, file-backed store that persists to `data/chroma_db/`.

4. **Ingest the documents**

   Run this once, and again any time the contents of `data/` change:

   ```bash
   python app/vector_init.py
   ```

   This loads every `.txt` file in `DATA_DIR`, chunks it, embeds the chunks, and writes them to both ChromaDB and Qdrant.

5. **Chat**

   ```bash
   python app/main.py
   ```

   A simple REPL: type a question, and it prints the retrieved chunks (with source and
   similarity score) first, then streams a grounded, cited answer token-by-token. If the
   documents don't contain the answer, it replies with a fixed fallback message and no
   citations, rather than guessing. Type `exit` to quit.

## Model choices

- **Embeddings and generation are decoupled** (`EMBED_MODEL` / `GEN_MODEL`), so an embedding model tuned for retrieval quality can be paired with a separate chat model tuned for answer quality, without code changes.
- Both talk through the **OpenAI SDK against an OpenAI-compatible base URL** (`OPENAI_BASE_URL`) rather than a vendor-specific client. This keeps the app provider-agnostic — it works unchanged against Ollama running locally, a self-hosted vLLM/LM Studio server, or real OpenAI/Azure endpoints, just by changing `.env`.
- The default `.env-example` points at **Ollama models** (`nomic-embed-text` for embeddings, `llama3:8b` for generation) since that's the cheapest way to develop and test the pipeline without API costs.
- Generation uses a low `TEMPERATURE` (default `0.2`) to favor grounded, consistent answers over creative variation, and the system prompt explicitly forbids answering from outside knowledge. If the retrieved context doesn't contain the answer, the model is required to reply with a fixed fallback sentence and no citations — this was tightened after testing showed the model would otherwise cite irrelevant sources alongside a refusal.

## Chunking rationale

Documents are split with a **recursive character splitter** (`app/chunking.py`), the same strategy popularized by LangChain's `RecursiveCharacterTextSplitter`:

1. Try to split on the highest-priority separator first — paragraph breaks (`\n\n`), then line breaks (`\n`), then sentence endings (`. `), then words (` `), then finally raw characters.
2. Any piece still larger than `CHUNK_SIZE` gets recursively split on the next, more granular separator.
3. Adjacent small pieces are merged back together up to `CHUNK_SIZE`, so a chunk isn't a single short line when it could hold several.

This keeps chunks close to natural language boundaries (paragraphs/sentences) instead of cutting mid-sentence at a fixed character offset, which preserves semantic coherence for embedding and retrieval.

After splitting, **overlap is added** (`CHUNK_OVERLAP` characters from the tail of one chunk are prepended to the next). This guards against an idea or reference sitting right at a chunk boundary — without overlap, a sentence split across two chunks can lose context in both halves.

Defaults are `CHUNK_SIZE=800`, `CHUNK_OVERLAP=120` (characters) — small enough to keep chunks topically focused for retrieval precision, with ~15% overlap to avoid losing boundary context, while staying well within any embedding model's input limit.

## Project structure

```
app/
  ingest.py        # loads .txt files from DATA_DIR
  chunking.py       # recursive splitter + overlap
  embeddings.py      # embed_texts / embed_query via OpenAI-compatible client
  vector_store.py     # writes chunks+embeddings to ChromaDB and Qdrant
  vector_init.py      # one-shot script: load -> chunk -> embed -> store
  retrieval.py       # search_chroma / search_qdrant
  generate.py        # builds the prompt and calls the chat model
  pipeline.py        # ask() ties retrieval + generation together
  main.py           # CLI chat loop
  config.py         # env-driven configuration
data/             # source documents + local ChromaDB persistence
docker_services/qdrant/  # Qdrant Docker Compose setup
scripts/
  test_queries.py     # runs 5 sample questions (incl. 1 off-topic) through the pipeline
```
