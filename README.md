# Python Ollama Chatbot

FastAPI backend that chats with a **local** LLM via [Ollama](https://ollama.com/). The assistant is prompted as a **Python tutor for beginners**, with per-user conversation memory and a bounded context window.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running
- A model pulled locally, e.g. `ollama pull llama3`

## Setup

```bash
cd chatbot
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Start Ollama (if not already running):

```bash
ollama serve
```

## Run the API

```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive OpenAPI docs, or call the chat endpoint manually:

```bash
curl -s -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo","message":"What is a Python list?"}'
```

Use the same `user_id` across requests to keep conversation context (trimmed to the last N messages; see `memory.py`).

## Project layout

| Path | Role |
|------|------|
| `main.py` | FastAPI app and `/chat` route |
| `schemas.py` | Request/response models |
| `memory.py` | In-memory history + context trimming |
| `services/ollama_service.py` | Ollama `/api/chat` client, system prompt, timeouts |

## License

Use and modify freely for learning.
