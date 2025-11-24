from typing import List
from util.embedding import embed_texts
from db.vector_store import VectorStore

class Retriever:
    def __init__(self, collection_name: str = "default", persist_dir: str = "index_data"):
        self.vs = VectorStore(collection_name=collection_name, persist_dir=persist_dir)

    async def search(self, query: str, top_k: int = 5):
        q_vec = embed_texts(query)
        hits = self.vs.search(q_vec, top_k=top_k)
        return hits