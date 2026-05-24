from io import BytesIO

from pypdf import PdfReader


def _load_txt_from_bytes(raw: bytes) -> str:
    return raw.decode("utf-8")


def _load_pdf_from_bytes(raw: bytes) -> str:
    reader = PdfReader(BytesIO(raw))
    parts: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            parts.append(page_text)
    return "\n".join(parts)


def extract_text(filename: str, raw: bytes) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        return _load_pdf_from_bytes(raw)
    if name.endswith(".txt"):
        return _load_txt_from_bytes(raw)
    raise ValueError(f"Unsupported file type: {filename}. Use .pdf or .txt")
