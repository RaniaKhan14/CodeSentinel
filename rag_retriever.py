import os
import pickle
import numpy as np
from rank_bm25 import BM25Okapi
import faiss
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document

class HybridRetriever:
    def __init__(self, corpus_file="data/best_practices.txt"):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = self._load_corpus(corpus_file)
        # BM25
        tokenized_corpus = [doc.page_content.split() for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_corpus)
        # FAISS
        embeddings = self.encoder.encode([doc.page_content for doc in self.documents])
        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype(np.float32))
    
    def _load_corpus(self, path):
        with open(path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        return [Document(page_content=line, metadata={"source": "best_practices"}) for line in lines]
    
    def retrieve(self, query: str, k: int = 3) -> str:
        # BM25
        bm25_scores = self.bm25.get_scores(query.split())
        top_bm25_idx = np.argsort(bm25_scores)[-k:][::-1]
        bm25_docs = [self.documents[i].page_content for i in top_bm25_idx]
        
        # FAISS
        query_emb = self.encoder.encode([query])
        distances, faiss_idx = self.index.search(query_emb.astype(np.float32), k)
        faiss_docs = [self.documents[i].page_content for i in faiss_idx[0]]
        
        # Merge and deduplicate
        combined = list(dict.fromkeys(bm25_docs + faiss_docs))
        return "\n".join([f"- {doc}" for doc in combined[:k]])

# Singleton for reuse
_retriever = None

def get_hybrid_retriever():
    global _retriever
    if _retriever is None:
        _retriever = HybridRetriever()
    return _retriever

def retrieve_best_practices(query: str) -> str:
    """Retrieve relevant coding best practices for a given code issue or concept."""
    retriever = get_hybrid_retriever()
    return retriever.retrieve(query, k=3)