"""Reusable RAG core for the PDF Chatbot project.

Pipeline: extract PDF text -> chunk -> embed -> index (Chroma) -> retrieve -> answer (Claude).

Dependencies:
    pip install chromadb sentence-transformers pypdf anthropic

Environment:
    ANTHROPIC_API_KEY must be set (never hardcode keys).
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    page: int


# --------------------------------------------------------------------------- #
# 1. Extraction
# --------------------------------------------------------------------------- #
def extract_pdf(path: str) -> list[tuple[int, str]]:
    """Return a list of (page_number, page_text) for a PDF file."""
    from pypdf import PdfReader

    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append((i, text))
    return pages


# --------------------------------------------------------------------------- #
# 2. Chunking (recursive-ish, with overlap)
# --------------------------------------------------------------------------- #
def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    """Split text into overlapping character windows, preferring sentence boundaries."""
    text = " ".join(text.split())  # normalize whitespace
    if len(text) <= size:
        return [text]
    chunks, start = [], 0
    while start < len(text):
        end = start + size
        # try to end on a sentence boundary within the window
        window = text[start:end]
        dot = window.rfind(". ")
        if dot > size * 0.5:
            end = start + dot + 1
        chunks.append(text[start:end].strip())
        start = end - overlap
    return [c for c in chunks if c]


def build_chunks(pdf_paths: list[str], size: int = 800, overlap: int = 100) -> list[Chunk]:
    """Extract and chunk a list of PDFs into Chunk objects with provenance metadata."""
    out: list[Chunk] = []
    for path in pdf_paths:
        source = os.path.basename(path)
        for page_num, page_text in extract_pdf(path):
            for piece in chunk_text(page_text, size, overlap):
                out.append(Chunk(text=piece, source=source, page=page_num))
    return out


# --------------------------------------------------------------------------- #
# 3. Indexing (Chroma + sentence-transformers)
# --------------------------------------------------------------------------- #
def build_index(chunks: list[Chunk], persist_dir: str = "./chroma_pdf",
                collection: str = "pdf_chatbot"):
    """Embed chunks and store them in a persistent Chroma collection. Returns the collection."""
    import chromadb
    from chromadb.utils import embedding_functions

    client = chromadb.PersistentClient(path=persist_dir)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    # Recreate for a clean index each run; in production, upsert instead.
    try:
        client.delete_collection(collection)
    except Exception:
        pass
    coll = client.create_collection(collection, embedding_function=embed_fn)

    coll.add(
        ids=[f"c{i}" for i in range(len(chunks))],
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "page": c.page} for c in chunks],
    )
    return coll


# --------------------------------------------------------------------------- #
# 4. Retrieval
# --------------------------------------------------------------------------- #
def retrieve(coll, query: str, k: int = 4):
    """Return list of (text, metadata, distance) for the top-k chunks."""
    res = coll.query(query_texts=[query], n_results=k)
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res.get("distances", [[0] * len(docs)])[0]
    return list(zip(docs, metas, dists))


# --------------------------------------------------------------------------- #
# 5. Generation (Claude), grounded with a "don't know" guard
# --------------------------------------------------------------------------- #
SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions using ONLY the provided context "
    "from the user's PDFs. If the context does not contain the answer, say you don't know. "
    "Cite the source file and page number for each claim, like (source.pdf, p.3)."
)


def answer(coll, query: str, k: int = 4, model: str = "claude-opus-4-8") -> dict:
    """Retrieve context and generate a grounded answer with citations."""
    hits = retrieve(coll, query, k)
    if not hits:
        return {"answer": "I don't have any indexed documents to answer from.", "citations": []}

    context_blocks = []
    citations = []
    for text, meta, _dist in hits:
        tag = f"({meta['source']}, p.{meta['page']})"
        context_blocks.append(f"{tag} {text}")
        citations.append(tag)

    context = "\n\n".join(context_blocks)
    user_msg = f"Context:\n{context}\n\nQuestion: {query}"

    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    resp = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    text_out = next((b.text for b in resp.content if b.type == "text"), "")
    return {"answer": text_out, "citations": sorted(set(citations))}


if __name__ == "__main__":
    # Tiny smoke test of chunking (no PDF / API key required)
    sample = "Sentence one. " * 200
    pieces = chunk_text(sample, size=300, overlap=50)
    print(f"chunk_text produced {len(pieces)} chunks; first is {len(pieces[0])} chars.")
