import shutil
from pathlib import Path

import chromadb

from config import CHROMA_BASE_DIR, COLLECTION_NAME, DEFAULT_TOP_K
from services.embedding_service import embed_query

_clients: dict[str, chromadb.PersistentClient] = {}


def _session_path(session_id: str) -> Path:
    return Path(CHROMA_BASE_DIR) / session_id


def get_client(session_id: str) -> chromadb.PersistentClient:
    if session_id not in _clients:
        path = _session_path(session_id)
        path.mkdir(parents=True, exist_ok=True)
        _clients[session_id] = chromadb.PersistentClient(path=str(path))
    return _clients[session_id]


def get_collection(session_id: str):
    client = get_client(session_id)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def add_chunks(session_id: str, ids: list[str], embeddings, documents: list[str]) -> None:
    collection = get_collection(session_id)
    if hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()
    elif embeddings and hasattr(embeddings[0], "tolist"):
        embeddings = [e.tolist() for e in embeddings]
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
    )


def query_chunks(session_id: str, query: str, n_results: int = DEFAULT_TOP_K) -> dict:
    collection = get_collection(session_id)
    query_embedding = embed_query(query)
    if hasattr(query_embedding, "tolist"):
        query_embedding = query_embedding.tolist()
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )


def delete_session_store(session_id: str) -> None:
    if session_id in _clients:
        del _clients[session_id]

    session_dir = _session_path(session_id)
    if session_dir.exists():
        shutil.rmtree(session_dir)
