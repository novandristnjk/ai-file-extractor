import os
from typing import List, Dict
import numpy as np
import faiss


class VectorStore:
    """Simple FAISS-backed vector store with in-memory metadata list and disk persistence."""

    def __init__(self, collection_name: str = "default", persist_dir: str = "index_data"):
        self.collection = collection_name
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)

        self.meta_path = os.path.join(persist_dir, f"{collection_name}_meta.npy")
        self.index_path = os.path.join(persist_dir, f"{collection_name}_faiss.index")

        self.metadata = []  # list of dicts with keys: text, payload
        self.index = None
        self.dim = None

        # Try to load existing
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            try:
                self.index = faiss.read_index(self.index_path)
                self.metadata = list(np.load(self.meta_path, allow_pickle=True))
                if self.metadata and "dim" in self.metadata[0]:
                    self.dim = int(self.metadata[0]["dim"])
            except Exception as e:
                print("Failed to load existing index:", e)
                self.index = None

    def upsert(self, texts: List[str], vectors: List[List[float]], metadatas: List[Dict]):
        assert len(texts) == len(vectors) == len(metadatas)

        vecs = np.array(vectors).astype("float32")
        n, dim = vecs.shape

        if self.index is None:
            # use inner-product (cosine similarity after normalization)
            self.dim = dim
            self.index = faiss.IndexFlatIP(dim)

        if vecs.shape[1] != self.dim:
            raise ValueError("Dimension mismatch")

        # normalize vectors
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        vecs = vecs / norms

        self.index.add(vecs)

        # store metadata
        for t, m in zip(texts, metadatas):
            entry = {"text": t, "payload": m, "dim": self.dim}
            self.metadata.append(entry)

    def search(self, query_vector, top_k=5):
        q = np.array(query_vector).astype("float32")

        if q.ndim == 1:
            q = q.reshape(1, -1)

        # normalize query
        q = q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-10)

        D, I = self.index.search(q, top_k)

        hits = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue

            entry = self.metadata[idx]
            hits.append({
                "text": entry["text"],
                "payload": entry["payload"],
                "score": float(score)
            })

        return hits

    def save(self):
        if self.index is not None:
            faiss.write_index(self.index, self.index_path)
            np.save(self.meta_path, np.array(self.metadata, dtype=object), allow_pickle=True)
