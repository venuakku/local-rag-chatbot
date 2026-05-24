def chunk_text(text: str) -> list[str]:
    raw_chunks = text.split("\n")
    cleaned_chunks: list[str] = []

    for chunk in raw_chunks:
        cleaned_chunk = chunk.strip()
        if cleaned_chunk:
            cleaned_chunks.append(cleaned_chunk)

    return cleaned_chunks
