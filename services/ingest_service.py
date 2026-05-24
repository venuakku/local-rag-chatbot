import uuid

from fastapi import HTTPException

from services.chunk_service import chunk_text
from services.document_service import extract_text
from services.embedding_service import embed_texts
from services.vector_store_service import add_chunks


def ingest_file(session_id: str, filename: str, raw: bytes) -> dict:
    if not session_id.strip():
        raise HTTPException(status_code=400, detail="session_id is required")

    try:
        text = extract_text(filename, raw)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from the file")

    chunks = chunk_text(text)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks produced from document")

    embeddings = embed_texts(chunks)
    prefix = uuid.uuid4().hex
    ids = [f"{prefix}_{i}" for i in range(len(chunks))]

    add_chunks(session_id, ids, embeddings, chunks)

    return {
        "status": "success",
        "chunks_added": len(chunks),
        "filename": filename,
    }
