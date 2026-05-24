import uuid

import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ingested_files" not in st.session_state:
    st.session_state.ingested_files = []


def reset_session():
    try:
        requests.post(
            f"{BACKEND_URL}/session/reset",
            json={"session_id": st.session_state.session_id},
            timeout=30,
        )
    except requests.RequestException:
        pass

    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.ingested_files = []
    st.session_state._uploaded_keys = set()


st.title("Local RAG Chatbot")

with st.sidebar:
    st.caption("Session")
    st.code(st.session_state.session_id[:8] + "...", language=None)

    if st.button("New session", use_container_width=True):
        reset_session()
        st.rerun()

    if st.session_state.ingested_files:
        st.subheader("Ingested files")
        for name in st.session_state.ingested_files:
            st.write(f"- {name}")

uploaded_file = st.file_uploader(
    "Upload document",
    type=["pdf", "txt"],
)

if uploaded_file is not None:
    upload_key = f"{st.session_state.session_id}:{uploaded_file.name}"

    if upload_key not in st.session_state.get("_uploaded_keys", set()):
        with st.spinner("Ingesting document..."):
            try:
                uploaded_file.seek(0)
                response = requests.post(
                    f"{BACKEND_URL}/ingest",
                    data={"session_id": st.session_state.session_id},
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type or "application/octet-stream",
                        )
                    },
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()
                st.success(
                    f"Added {data['chunks_added']} chunks from {data['filename']}"
                )
                st.session_state.ingested_files.append(data["filename"])

                if "_uploaded_keys" not in st.session_state:
                    st.session_state._uploaded_keys = set()
                st.session_state._uploaded_keys.add(upload_key)
            except requests.RequestException as exc:
                detail = ""
                if exc.response is not None:
                    try:
                        detail = exc.response.json().get("detail", "")
                    except Exception:
                        detail = exc.response.text
                st.error(detail or "Failed to ingest. Is the API running on port 8000?")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("Retrieved sources"):
                for i, source in enumerate(msg["sources"], 1):
                    st.markdown(f"**Source {i}**")
                    st.write(source)

if prompt := st.chat_input("Ask a question about your documents"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/chat-rag",
                    json={
                        "session_id": st.session_state.session_id,
                        "message": prompt,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()
                reply = data["reply"]
                sources = data.get("sources", [])
                st.write(reply)
                if sources:
                    with st.expander("Retrieved sources"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"**Source {i}**")
                            st.write(source)
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply, "sources": sources}
                )
            except requests.RequestException as exc:
                detail = ""
                if exc.response is not None:
                    try:
                        detail = exc.response.json().get("detail", "")
                    except Exception:
                        detail = exc.response.text
                err = detail or "Failed to get answer. Upload a document and ensure the API is running."
                st.error(err)
                st.session_state.messages.append(
                    {"role": "assistant", "content": err}
                )
