# Glossary — AI Engineering Bootcamp

Key terms across the curriculum, grouped by area. Week references point to where the term is
taught.

## Python & Data (Week 1)
- **DataFrame** — a 2D labeled table (rows × columns) in Pandas, built on NumPy arrays.
- **Vectorization** — applying an operation to a whole array at once (in C) instead of a Python
  loop; the basis of NumPy/Pandas performance.
- **Broadcasting** — NumPy's rules for operating on arrays of different shapes without copying.
- **REST API** — an HTTP interface exposing resources via GET/POST/PUT/DELETE.
- **JSON** — a text format for structured data; maps to Python dicts/lists.
- **SQL injection** — a vulnerability from concatenating untrusted input into SQL; prevented by
  parameterized queries.

## Machine Learning (Week 2)
- **Supervised learning** — learning a mapping from inputs to labeled outputs (classification,
  regression).
- **Unsupervised learning** — finding structure in unlabeled data (e.g. clustering).
- **Data leakage** — when information unavailable at prediction time (or from the test set) leaks
  into training, inflating metrics.
- **Feature engineering** — transforming raw data into model-ready inputs (encoding, scaling,
  new features).
- **Train/test split** — partitioning data to estimate out-of-sample performance.
- **Cross-validation** — repeated train/validate splits (k-fold) for a robust performance estimate.
- **Overfitting / underfitting** — modeling noise vs failing to capture signal.
- **Precision / recall / F1** — classification metrics from the confusion matrix.
- **ROC-AUC** — threshold-independent ranking quality of a classifier.
- **Hyperparameter tuning** — searching model settings (GridSearchCV / RandomizedSearchCV).

## GenAI & LLMs (Week 3)
- **Transformer** — the neural architecture behind modern LLMs, based on self-attention.
- **Self-attention** — mechanism where each token weighs the relevance of every other token
  (Q, K, V; scaled dot-product).
- **Token** — a sub-word unit of text; models are priced and limited per token.
- **Embedding** — a vector representation of text where similar meanings are close together.
- **Cosine similarity** — similarity of two vectors by the cosine of the angle between them.
- **Vector database** — stores embeddings for fast nearest-neighbor (similarity) search.
- **ANN (Approximate Nearest Neighbor)** — fast, slightly-inexact similarity search (HNSW, IVF).
- **Prompt engineering** — structuring inputs (zero/few-shot, chain-of-thought, system prompts)
  for reliable outputs.
- **Structured output** — constraining a model to return a JSON schema instead of free text.
- **Tool / function calling** — the model requests that your code run a function, then uses the
  result.
- **Agent** — an LLM that decides and executes actions via tools in a loop.
- **MCP (Model Context Protocol)** — an open standard for connecting LLM apps to tools,
  resources, and prompts.
- **Multi-agent system** — several role-specialized agents composed into a workflow.
- **Context window** — the maximum tokens a model can attend to in one request.
- **Hallucination** — a fluent but unsupported/incorrect model output.

## RAG (Week 4)
- **RAG (Retrieval-Augmented Generation)** — retrieve relevant documents, then generate an answer
  grounded in them.
- **Chunking** — splitting documents into retrievable units (fixed, overlap, recursive, semantic).
- **BM25** — a classic keyword-ranking function; captures exact-term relevance.
- **Hybrid search** — combining vector (semantic) and keyword (BM25) retrieval.
- **Reciprocal Rank Fusion (RRF)** — merging multiple ranked lists without score normalization.
- **Reranking** — re-ordering candidates with a cross-encoder that reads query + doc jointly.
- **Cross-encoder** — a model scoring a (query, document) pair together; precise but slow.
- **Metadata filtering** — restricting retrieval by structured fields (source, date, access).
- **recall@k / precision@k / MRR** — retrieval-quality metrics.
- **Faithfulness** — whether a generated answer is supported by the retrieved context.

## Automation (Week 5)
- **n8n** — an open-source workflow-automation tool (nodes, triggers, connections).
- **Trigger** — a node that starts a workflow (manual, webhook, schedule, IMAP, chat).
- **Webhook** — an HTTP endpoint that receives event payloads to start/continue a workflow.
- **Credential store** — n8n's encrypted secret storage; keys never live in node fields.

## Deployment & Ops (Week 6)
- **Container / Docker image** — a portable, reproducible package of app + dependencies.
- **ASGI / uvicorn / gunicorn** — Python async web-server plumbing for FastAPI.
- **Pydantic** — data-validation library used to validate API request/response bodies.
- **CI/CD** — automated linting, testing, and deployment on each change.
- **Health check** — an endpoint (`/health`) platforms poll to detect readiness.
- **Secret manager** — a service (AWS Secrets Manager, GCP Secret Manager) that injects secrets
  at runtime instead of baking them into images.
- **LLMOps** — practices for operating LLM apps: evals, prompt versioning, cost/latency
  monitoring, observability.
- **Cold start** — latency when a scaled-to-zero service spins up for the first request.
