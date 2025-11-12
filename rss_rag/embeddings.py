# rss_rag/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

class LocalEmbedder:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return np.array(embeddings)