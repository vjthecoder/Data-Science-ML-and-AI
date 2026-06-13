# Week 4 Solutions

Reference solutions for `../assignments/week04_assignments.md`. Attempt them first.

---

## Solution 1 — RAG Architecture

```python
import numpy as np, os

docs = [...]  # 10 documents
def embed(t):
    v = np.zeros(64)
    for w in t.lower().split(): v[hash(w) % 64] += 1.0
    n = np.linalg.norm(v); return v / n if n else v
vecs = np.array([embed(d) for d in docs])

def rag_answer(q, k=2, threshold=0.1):
    qv = embed(q); sims = vecs @ qv
    top = np.argsort(sims)[::-1][:k]
    if sims[top[0]] < threshold:
        return "I don't know."
    context = "\n".join(docs[i] for i in top)
    prompt = f"Answer using ONLY this context:\n{context}\n\nQuestion: {q}"
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return prompt  # offline fallback
    import anthropic
    r = anthropic.Anthropic().messages.create(
        model="claude-opus-4-8", max_tokens=512,
        messages=[{"role": "user", "content": prompt}])
    return next(b.text for b in r.content if b.type == "text")
```
**RAG vs fine-tuning:** RAG for knowledge that changes or needs citations (cheap to re-index);
fine-tuning for behavior/format/style the model should internalize. They're complementary.

---

## Solution 2 — Chunking

See notebook 02 for `chunk_fixed` and `chunk_recursive`. Heading-aware:
```python
import re
def chunk_markdown(md):
    parts = re.split(r"(?m)^(#{1,6} .+)$", md)
    chunks, heading = [], ""
    for seg in parts:
        if re.match(r"^#{1,6} ", seg or ""):
            heading = seg.strip("# ").strip()
        elif seg and seg.strip():
            chunks.append({"text": seg.strip(), "metadata": {"section": heading}})
    return chunks
```
Overlap retrieves boundary-spanning answers because the second chunk repeats the tail of the
first, so the full sentence appears intact in at least one chunk.

---

## Solution 3 — Vector Search

```python
import faiss, numpy as np, chromadb
# FAISS
idx = faiss.IndexFlatIP(emb.shape[1]); idx.add(emb.astype("float32"))
scores, ids = idx.search(query_vec.astype("float32").reshape(1, -1), 3)

# Chroma persistence
client = chromadb.PersistentClient(path="./chroma_db")
coll = client.get_or_create_collection("kb")
coll.add(ids=[...], documents=[...])
# Re-open later: chromadb.PersistentClient(path="./chroma_db").get_collection("kb") -> data persists

# Threshold
def retrieve(coll, q, k=3, max_distance=0.6):
    r = coll.query(query_texts=[q], n_results=k)
    return [(d, dist) for d, dist in zip(r["documents"][0], r["distances"][0]) if dist <= max_distance]
```

---

## Solution 4 — Hybrid Search & Reranking

See notebook 04 (`bm25_scores`, `rrf`) and lab 3 for full code. Hybrid beats vector-only on
queries containing exact IDs/codes (e.g. "X-450") because BM25 matches the literal token that a
semantic embedding may dilute. Cross-encoder reranking then lifts precision@3 by re-scoring the
fused candidates with joint query-document attention.

---

## Solution 5 — Metadata Filtering

See notebook 05. OR filter:
```python
def search(query, where_in=None, k=2):
    items = corpus
    if where_in:
        field, allowed = where_in
        items = [c for c in corpus if c.get(field) in allowed]
    ...
search("refund", where_in=("product", {"Pro", "Enterprise"}))
```
Post-filtering can return < k results because filtering happens AFTER the top-k cut — if few of
the top-k pass the filter, you're left with too few. Pre-filtering searches only the eligible
subset, guaranteeing k results when enough eligible docs exist.

---

## Solution 6 — RAG Evaluation

See notebook 06 (`recall_at_k`, `precision_at_k`, `mrr`). Faithfulness proxy:
```python
def faithfulness_proxy(answer, context):
    a = set(answer.lower().split()); c = set(context.lower().split())
    return len(a & c) / len(a) if a else 0.0
```
Report mean metrics across the eval set; ship the chunk config that maximizes recall without
dropping faithfulness below your bar (e.g. 0.9).

---

## Solution 7 — PDF Chatbot Project

Use `projects/pdf_chatbot/` as-is. Citations and the "I don't know" path are implemented in
`rag_core.answer` (empty retrieval) and can be extended with a distance threshold in `retrieve`.
Document architecture, 3 example Q&A, and limitations (e.g. scanned PDFs need OCR; tables chunk
poorly; very long PDFs need better chunking) in the project README.
