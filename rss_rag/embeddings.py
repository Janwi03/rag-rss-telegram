from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize embedding model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
print(f"🔹 Loading embedding model: {model_name}")

try:
    embedding_model = SentenceTransformer(model_name)
except Exception as e:
    print(f"❌ Failed to load embedding model: {e}")
    embedding_model = None


def generate_embedding(text: str) -> np.ndarray:
    """
    Generates a numerical embedding vector for the given text.
    Used for duplicate detection and semantic similarity in FAISS.
    """
    if not text.strip():
        print("⚠️ Empty text received for embedding generation.")
        return np.zeros((384,), dtype=np.float32)

    if embedding_model is None:
        print("⚠️ Embedding model not initialized. Returning zeros.")
        return np.zeros((384,), dtype=np.float32)

    embedding = embedding_model.encode([text])[0]
    return np.array(embedding, dtype=np.float32)