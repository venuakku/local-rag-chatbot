# Local RAG Chatbot

Upload documents (PDF/TXT), ask questions grounded in your files. Uses **FastAPI**, **Streamlit**, **Ollama**, **ChromaDB**, and **Hugging Face** embeddings (`all-MiniLM-L6-v2`).

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) with `llama3`: `ollama pull llama3`

## Setup

```bash
cd chatbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

**Terminal 1 — Ollama**

```bash
ollama serve
```

**Terminal 2 — API**

```bash
cd chatbot
source .venv/bin/activate
uvicorn main:app --reload
```

**Terminal 3 — Streamlit UI**

```bash
cd chatbot
source .venv/bin/activate
streamlit run streamlit_app.py
```

Open [http://127.0.0.1:8501](http://127.0.0.1:8501).

1. Upload a `.pdf` or `.txt`
2. Ask questions about the document
3. **New session** clears vectors for that session (`data/chroma/<session_id>/`)

## API

| Endpoint | Purpose |
|----------|---------|
| `POST /ingest` | Form: `session_id`, `file` |
| `POST /chat-rag` | JSON: `session_id`, `message` |
| `POST /session/reset` | JSON: `session_id` |

Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Project layout

```
chatbot/
  main.py              # FastAPI routes
  streamlit_app.py     # UI
  config.py            # Chroma paths
  schemas.py
  services/
    document_service.py
    chunk_service.py
    embedding_service.py
    vector_store_service.py
    ingest_service.py
    rag_service.py
    ollama_service.py
```

Vectors are stored under `data/chroma/<session_id>/` (gitignored).
