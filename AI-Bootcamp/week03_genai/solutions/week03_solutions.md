# Week 3 Solutions

Reference solutions for `../assignments/week03_assignments.md`. Attempt the assignments first.

---

## Solution 1 — Transformers & Attention

```python
import numpy as np

def softmax(x, axis=-1):
    e = np.exp(x - x.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

def attention(Q, K, V, causal=False):
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)
    if causal:
        n = scores.shape[0]
        scores[np.triu(np.ones((n, n)), k=1).astype(bool)] = -np.inf
    weights = softmax(scores)
    return weights @ V, weights

def multihead(Q, K, V, heads=2):
    d = Q.shape[-1]; h = d // heads
    outs = [attention(Q[:, i*h:(i+1)*h], K[:, i*h:(i+1)*h], V[:, i*h:(i+1)*h])[0]
            for i in range(heads)]
    return np.concatenate(outs, axis=-1)
```
**Scaling rationale:** dot products grow with `d_k`; without `1/√d_k` the softmax saturates,
producing near-one-hot weights and tiny gradients, which destabilizes training.

---

## Solution 2 — Tokens & Embeddings

```python
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")

sents = ["I love pizza", "Pizza is great", "Pasta is delicious",
         "Stocks fell today", "Markets dropped", "Equities slid",
         "My cat sleeps", "The dog runs"]
emb = model.encode(sents, normalize_embeddings=True)
sim = util.cos_sim(emb, emb)          # 8x8 matrix; food/finance pairs score highest

for q in ["tasty Italian dinner", "the market crashed", "a sleepy pet"]:
    qe = model.encode(q, normalize_embeddings=True)
    scores = util.cos_sim(qe, emb)[0]
    top2 = scores.argsort(descending=True)[:2]
    print(q, "->", [sents[i] for i in top2])
```
Token-count difference: Anthropic's `count_tokens` vs OpenAI's `tiktoken` differ because each
provider uses a different tokenizer/vocabulary — always match the tokenizer to the model.

---

## Solution 3 — Vector Databases

```python
import faiss, numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
docs = [f"document about topic {i%4}" for i in range(20)]
emb = model.encode(docs, normalize_embeddings=True).astype("float32")

flat = faiss.IndexFlatIP(emb.shape[1]); flat.add(emb)
hnsw = faiss.IndexHNSWFlat(emb.shape[1], 32); hnsw.add(emb)

q = model.encode("topic 2", normalize_embeddings=True).astype("float32").reshape(1, -1)
_, exact = flat.search(q, 3)
_, approx = hnsw.search(q, 3)
recall = len(set(exact[0]) & set(approx[0])) / 3
print("recall@3:", recall)

# Chroma with metadata filter
import chromadb
client = chromadb.Client()
coll = client.create_collection("docs")
coll.add(ids=[str(i) for i in range(20)], documents=docs,
         metadatas=[{"category": f"cat{i%2}"} for i in range(20)])
res = coll.query(query_texts=["topic 2"], n_results=3, where={"category": "cat0"})
print(res["metadatas"])  # all cat0
```

---

## Solution 4 — Prompt Engineering

```python
import anthropic, json
client = anthropic.Anthropic()

SYSTEM = "Classify the ticket as one of: billing, technical, account, other. Reply with one word."

def classify(text):
    r = client.messages.create(model="claude-opus-4-8", max_tokens=16,
                               system=SYSTEM, messages=[{"role": "user", "content": text}])
    return next(b.text for b in r.content if b.type == "text").strip().lower()

eval_set = [("I was charged twice", "billing"), ("app crashes on login", "technical"),
            ("reset my password", "account"), ("love your product", "other")]
acc = sum(classify(t) == y for t, y in eval_set) / len(eval_set)
print("accuracy:", acc)
```
Few-shot generally raises accuracy and reduces format errors. For the structured version, add
`output_config={"format": {"type": "json_schema", "schema": {...}}}` with `category` and
`confidence` fields.

---

## Solution 5 — Tool / Function Calling

See `../labs/lab5_simple_agent.py` for the full manual-loop implementation. Key points:
append `{"role": "assistant", "content": resp.content}`, then a `user` message with one
`tool_result` per `tool_use` (matching `tool_use_id`); return `is_error: true` on failures;
cap iterations with `max_steps`.

---

## Solution 6 — MCP

```python
class MiniMCPServer:
    def __init__(self, name): self.name=name; self.tools={}; self.resources={}
    def tool(self, fn): self.tools[fn.__name__]=fn; return fn
    def list_tools(self): return list(self.tools)
    def call_tool(self, name, **kw): return self.tools[name](**kw)

s = MiniMCPServer("demo")
s.tool(lambda a, b: a + b).__name__  # or use decorators for add/subtract/multiply

def client_call(server, name, **kwargs):
    assert name in server.list_tools()
    return server.call_tool(name, **kwargs)
```
**MCP vs one-off integration:** with function calling you re-implement each integration per app;
with MCP you write a server once and any MCP client reuses it. Security benefit: credentials and
side effects live in the server/host, never in the model's context — so a prompt-injected model
can't read the secret.

---

## Solution 7 — Multi-Agent Systems

```python
def researcher(topic): return [f"Fact {i} about {topic}" for i in range(1, 4)]
def writer(notes): return "Draft: " + "; ".join(notes)
def reviewer(draft): return draft.replace("Draft:", "Final:")
def fact_checker(notes): return [n for n in notes if "Fact 2" in n]  # flag for citation

def orchestrate(subtopics):
    if len(subtopics) <= 2:
        return [writer(researcher(t)) for t in subtopics]       # sequential
    import concurrent.futures as cf
    with cf.ThreadPoolExecutor() as pool:
        return list(pool.map(lambda t: writer(researcher(t)), subtopics))  # parallel
```
Multi-agent wins when subtasks are independent and parallelizable, or when a fresh-context
reviewer catches the writer's errors. It's overhead for a simple single-step task (e.g. "classify
this sentence"), where one well-prompted call is cheaper and faster.
