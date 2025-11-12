# rss_rag/embeddings.py

from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the local embedding model (use a lightweight one)
model_name = "sentence-transformers/all-MiniLM-L6-v2"

print(f"🔹 Loading embedding model: {model_name}")
embedding_model = SentenceTransformer(model_name)

def generate_embedding(text: str):
    """
    Generates a numerical embedding vector for the given text.
    Used for duplicate detection and semantic similarity in FAISS.
    """
    if not text.strip():
        return np.zeros((384,), dtype=np.float32)  # all-MiniLM-L6-v2 outputs 384-dim embeddings
    embedding = embedding_model.encode([text])[0]
    return np.array(embedding, dtype=np.float32)