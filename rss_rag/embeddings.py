# rss_rag/embeddings.py
"""
Defensive embedding module.
Always defines `generate_embedding` at import time (no ImportError).
Attempts to load SentenceTransformer; if it fails, falls back to a zero-vector stub.
"""

import numpy as np
import traceback

# DIMENSION — keep consistent with your FAISS store
EMB_DIM = 384

# --- 1) Define a safe stub immediately so import never fails ---
def _stub_generate_embedding(text: str) -> np.ndarray:
    """Return a zero vector stub. Safe fallback if model not available."""
    if not isinstance(text, str) or not text.strip():
        return np.zeros((EMB_DIM,), dtype=np.float32)
    return np.zeros((EMB_DIM,), dtype=np.float32)

# export name (will be overridden if model loads successfully)
generate_embedding = _stub_generate_embedding

# --- 2) Try to load the real model (non-fatal if it fails) ---
try:
    from sentence_transformers import SentenceTransformer
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    print(f"🔹 Attempting to load embedding model: {MODEL_NAME}")
    _embedding_model = SentenceTransformer(MODEL_NAME)
    print("✅ Embedding model loaded successfully.")

    def _real_generate_embedding(text: str) -> np.ndarray:
        if not isinstance(text, str) or not text.strip():
            return np.zeros((EMB_DIM,), dtype=np.float32)
        emb = _embedding_model.encode([text])[0]
        return np.array(emb, dtype=np.float32)

    # override stub with the real function
    generate_embedding = _real_generate_embedding

except Exception as e:
    # keep the stub; print clear diagnostics for CI logs
    print("❌ Failed to load SentenceTransformer for embeddings.")
    print("❌ Exception traceback:")
    traceback.print_exc()
    print("⚠️ Falling back to zero-vector generate_embedding (stub).")