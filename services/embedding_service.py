from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list[str]):
    return model.encode(texts, convert_to_numpy=True)


def embed_query(query: str):
    return model.encode(query, convert_to_numpy=True)
