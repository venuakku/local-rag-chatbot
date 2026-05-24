from fastapi import HTTPException

from services.ollama_service import ask_ollama
from services.vector_store_service import query_chunks


def ask_rag(query: str, session_id: str) -> dict:
    if not session_id.strip():
        raise HTTPException(status_code=400, detail="session_id is required")

    results = query_chunks(session_id, query)

    retrieved_docs = results.get("documents", [[]])[0]
    if not retrieved_docs:
        return {
            "reply": "I could not find the answer in the provided documents.",
            "sources": [],
        }

    context = "\n".join(retrieved_docs)
    sources = [doc[:300] + ("..." if len(doc) > 300 else "") for doc in retrieved_docs]

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant.\n"
                "Answer ONLY using the provided context.\n"
                "If answer is not in context, say:\n"
                "'I could not find the answer in the provided documents.'"
            ),
        },
        {
            "role": "user",
            "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{query}",
        },
    ]

    response = ask_ollama(messages)

    return {
        "reply": response,
        "sources": sources,
    }
