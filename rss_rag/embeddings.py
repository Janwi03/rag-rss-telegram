"""
Defensive embedding module.
Ensures `generate_embedding` is always available.
If SentenceTransformer fails to load, it falls back to a safe zero-vector stub.
"""

import numpy as np
import traceback

# ----------------------------------------------------
# EMBEDDING DIMENSION (must match your FAISS store)
# ----------------------------------------------------
EMB_DIM = 384


# ----------------------------------------------------
# 1️⃣ Define a safe stub immediately (always available)
# ----------------------------------------------------
def _stub_generate_embedding(text: str) -> np.ndarray:
    """Return a zero vector if the model isn't available or text is empty."""
    if not isinstance(text, str) or not text.strip():
        return np.zeros((EMB_DIM,), dtype=np.float32)
    return np.zeros((EMB_DIM,), dtype=np.float32)


# Export the stub by default
generate_embedding = _stub_generate_embedding


# ----------------------------------------------------
# 2️⃣ Attempt to load the real SentenceTransformer model
# ----------------------------------------------------
try:
    from sentence_transformers import SentenceTransformer

    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    print(f"🔹 Loading embedding model: {MODEL_NAME} ...")

    _embedding_model = SentenceTransformer(MODEL_NAME)
    print("✅ Embedding model loaded successfully.")

    def _real_generate_embedding(text: str) -> np.ndarray:
        if not isinstance(text, str) or not text.strip():
            return np.zeros((EMB_DIM,), dtype=np.float32)
        emb = _embedding_model.encode([text])[0]
        return np.array(emb, dtype=np.float32)

    # Override stub with the real embedding generator
    generate_embedding = _real_generate_embedding

except Exception as e:
    print("⚠️ Using fallback stub for embeddings — model load failed.")
    print("   Reason:", e)
    traceback.print_exc(limit=1)


# ----------------------------------------------------
# 3️⃣ Final safety: ensure function exists (for CI/CD)
# ----------------------------------------------------
if not callable(generate_embedding):
    print("🚨 CRITICAL: generate_embedding was undefined — restoring stub.")
    generate_embedding = _stub_generate_embedding