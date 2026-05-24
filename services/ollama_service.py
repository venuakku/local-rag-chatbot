import requests
from fastapi import HTTPException

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"
TIMEOUT_SECONDS = 120


def ask_ollama(messages: list) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        reply = data["message"]["content"].strip()
        if not reply:
            return (
                "I could not generate a response. "
                "Try rephrasing or shortening your question."
            )
        return reply
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Model timed out. Please try again.")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail="Model service unavailable.")
