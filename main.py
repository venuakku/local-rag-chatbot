from fastapi import FastAPI
from schemas import ChatRequest, ChatResponse
from memory import get_memory, trim_history
from services.ollama_service import ask_ollama, SYSTEM_PROMPT

app = FastAPI()


@app.get("/")
def home():
    return {"status": 200, "message": "Live"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    history = get_memory(request.user_id)

    if not history:
        history.append({"role": "system", "content": SYSTEM_PROMPT})

    history.append({"role": "user", "content": request.message})
    trim_history(history)  # limit before sending to model

    reply = ask_ollama(history)

    history.append({"role": "assistant", "content": reply})
    trim_history(history)  # keep store bounded

    return ChatResponse(reply=reply)