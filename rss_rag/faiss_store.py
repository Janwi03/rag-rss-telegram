# rss_rag/faiss_store.py

import faiss
import numpy as np
import os
import pickle

class FAISSStore:
    def __init__(self, dim=384, index_path="data/faiss_index.bin", meta_path="data/meta.pkl"):
        self.dim = int(dim)  # ✅ ensure dimension is an integer
        self.index_path = index_path
        self.meta_path = meta_path

        # Create data folder if not exists
        os.makedirs(os.path.dirname(index_path), exist_ok=True)

        # Load existing index if present
        if os.path.exists(index_path) and os.path.exists(meta_path):
            print("🔄 Loading existing FAISS index...")
            self.index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            print("🆕 Creating new FAISS index...")
            self.index = faiss.IndexFlatIP(self.dim)  # ✅ now guaranteed int
            self.metadata = []

    def add(self, embeddings, metas):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.metadata.extend(metas)
        self.save()

    def search(self, query_emb, top_k=3):
        query_emb = np.array(query_emb).astype("float32")
        scores, indices = self.index.search(query_emb, top_k)
        results = []
        for idx_list in indices:
            results.append([self.metadata[i] for i in idx_list if i < len(self.metadata)])
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)