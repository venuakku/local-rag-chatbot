from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    ChatResponse,
    IngestResponse,
    RagChatRequest,
    SessionResetRequest,
    SessionResetResponse,
)
from services.ingest_service import ingest_file
from services.rag_service import ask_rag
from services.vector_store_service import delete_session_store

app = FastAPI(title="Local RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"status": "ok", "message": "Local RAG API"}


@app.post("/chat-rag", response_model=ChatResponse)
def chat_rag(request: RagChatRequest):
    result = ask_rag(request.message, request.session_id)
    return ChatResponse(reply=result["reply"], sources=result["sources"])


@app.post("/ingest", response_model=IngestResponse)
async def ingest(
    session_id: str = Form(...),
    file: UploadFile = File(...),
):
    contents = await file.read()
    result = ingest_file(session_id, file.filename or "upload", contents)
    return IngestResponse(**result)


@app.post("/session/reset", response_model=SessionResetResponse)
def session_reset(request: SessionResetRequest):
    if not request.session_id.strip():
        raise HTTPException(status_code=400, detail="session_id is required")

    delete_session_store(request.session_id)
    return SessionResetResponse(status="cleared")
