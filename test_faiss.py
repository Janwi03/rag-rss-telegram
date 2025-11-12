from rss_rag.embeddings import LocalEmbedder
from rss_rag.faiss_store import FAISSStore

embedder = LocalEmbedder()
store = FAISSStore()

texts = [
    "AI is transforming healthcare.",
    "Stocks fell sharply in global markets today.",
    "New study shows AI improves diagnosis accuracy."
]

embs = embedder.embed_texts(texts)
metas = [{"title": f"Article {i+1}", "text": t} for i, t in enumerate(texts)]

store.add(embs, metas)

query = embedder.embed_texts("AI in medicine and diagnosis.")
results = store.search(query, top_k=2)

print(results)