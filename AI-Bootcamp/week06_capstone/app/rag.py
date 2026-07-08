"""RAG knowledge base for the AI Career Coach.

Indexes career/industry knowledge documents and retrieves relevant context to ground the
coach's advice. Uses a lightweight in-memory store with a pluggable embedding backend so the
app runs offline; swap in Chroma + sentence-transformers for production.
"""

from __future__ import annotations

import os

# Seed knowledge base; in production, load from files / a managed vector DB.
DEFAULT_KB = [
    "AI Engineer roles typically require Python, ML fundamentals, and experience deploying models.",
    "RAG (retrieval-augmented generation) is a highly in-demand skill for LLM application roles.",
    "Strong candidates show a public GitHub portfolio with clean commits, tests, and docs.",
    "Cloud deployment skills (Docker, AWS/GCP) materially increase AI engineering job prospects.",
    "Behavioral interviews assess communication, ownership, and collaboration, not just coding.",
    "Fine-tuning (LoRA/QLoRA) and evaluation (RAGAS, LLM-as-judge) are increasingly expected.",
]


def _hash_embed(text: str, dim: int = 256):
    import numpy as np

    v = np.zeros(dim)
    for w in text.lower().split():
        v[hash(w) % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n else v


class KnowledgeBase:
    """Minimal vector store. Falls back to hash embeddings when no embedding model is set."""

    def __init__(self, docs: list[str] | None = None, use_sentence_transformers: bool = False):
        import numpy as np

        self.docs = list(docs or DEFAULT_KB)
        self._model = None
        if use_sentence_transformers:
            try:
                from sentence_transformers import SentenceTransformer

                self._model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception:
                self._model = None  # fall back to hash embeddings
        self.vecs = np.array([self._embed(d) for d in self.docs])

    def _embed(self, text: str):
        if self._model is not None:
            return self._model.encode(text, normalize_embeddings=True)
        return _hash_embed(text)

    def retrieve(self, query: str, k: int = 3) -> list[str]:
        import numpy as np

        q = self._embed(query)
        sims = self.vecs @ q
        top = np.argsort(sims)[::-1][:k]
        return [self.docs[i] for i in top]


def build_context(query: str, kb: KnowledgeBase | None = None, k: int = 3) -> str:
    kb = kb or KnowledgeBase(use_sentence_transformers=bool(os.environ.get("USE_ST")))
    return "\n".join(f"- {d}" for d in kb.retrieve(query, k))


if __name__ == "__main__":
    print(build_context("How do I become an AI engineer?"))
