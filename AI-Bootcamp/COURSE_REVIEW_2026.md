# Course Review & Redesign — AI Engineering Bootcamp 2026

A critical review of the 6-week curriculum from the perspective of leading AI educators
(Andrew Ng, Andrej Karpathy, Jeremy Howard, Chip Huyen, Sebastian Raschka), followed by
concrete redesign recommendations to make this a top-tier 2026 AI Engineering bootcamp.

---

## 1. Missing Concepts

- **Math foundations module (Week 0):** Linear algebra (vectors, matrices, dot products),
  probability/statistics (distributions, Bayes' theorem), and calculus intuition (gradients)
  are assumed but never taught. Karpathy/Ng both emphasize "first principles" understanding.
- **Neural networks from scratch:** No module builds a neural net (forward/backward pass,
  backprop) in raw NumPy/PyTorch before jumping to transformers — students won't understand
  *why* transformers work.
- **PyTorch/training fundamentals:** No coverage of autograd, training loops, loss functions,
  optimizers (SGD/Adam), overfitting/regularization — core ML engineering skills.
- **LLM fine-tuning & PEFT:** No LoRA/QLoRA, instruction tuning, or RLHF/DPO overview —
  increasingly expected of "AI Engineers" in 2026.
- **Evaluation & observability for LLM apps:** No systematic coverage of LLM evals (e.g.,
  using `promptfoo`, `ragas`, LangSmith/Arize/Phoenix tracing), guardrails, or hallucination
  detection.
- **Data engineering basics:** No coverage of data pipelines, Airflow/Prefect, or working with
  larger-than-memory data (DuckDB, Polars, Spark basics).
- **MLOps / LLMOps:** No model versioning (MLflow), experiment tracking, CI for ML, or
  monitoring drift in production.
- **Security for AI apps:** No prompt injection defenses, PII redaction, or secure handling of
  user-uploaded files (relevant to Week 6 capstone resume upload).
- **Cost & latency optimization:** No module on token cost management, caching, streaming
  responses, batching — a daily concern for AI engineers.

## 2. Weak Explanations

- Week 3's attention/transformer module is listed as a single notebook — Karpathy-style
  "build it from scratch" (e.g., a tiny GPT, "makemore"-style) is far more effective than
  diagram-only explanations.
- Vector database coverage is shallow — needs a hands-on comparison of indexing strategies
  (HNSW vs IVF), not just "similarity search basics."
- "MCP overview" is a single notebook for a complex, fast-evolving protocol — should be a
  full hands-on lab building a real MCP server + client.
- Prompt engineering needs structured eval-driven iteration (write prompt -> run eval set ->
  measure -> iterate), not just technique lists.

## 3. Missing Projects

- A from-scratch micro neural network / micro-GPT project (Karpathy-style "nanoGPT" mini).
- A fine-tuning project (LoRA on a small open model for a domain-specific task).
- An evaluation harness project: build a test suite that scores a RAG/agent pipeline.
- A production observability project: instrument an LLM app with tracing + dashboards.
- A data pipeline project: scheduled ingestion -> transformation -> vector store update.
- An agent-with-memory project (persistent conversational memory, not just single-turn tools).

## 4. Industry Gaps

- No exposure to **Polars/DuckDB** (rapidly replacing Pandas for performance-sensitive work).
- No **Docker Compose multi-service** setup (API + vector DB + frontend) — Week 6 only
  mentions Docker generically.
- No **CI/CD for ML/AI code** (this very repo lacked it until this review — now addressed).
- No **cloud cost awareness** — students should learn to estimate LLM API costs at scale.
- No **team workflow simulation** — code review, PRs, issue tracking (now addressed via OSS
  infra below).

## 5. Hiring Market Expectations (2026)

Based on current "AI Engineer" job postings, candidates are expected to:
- Be fluent in **Python + at least one of PyTorch/TF** for model-level understanding
- Build and **evaluate** RAG/agent systems, not just demo them
- Know **vector DBs, hybrid search, and reranking** in depth
- Demonstrate **production deployment** (Docker, cloud, CI/CD, monitoring)
- Show **fine-tuning experience** (LoRA/QLoRA) even at small scale
- Have a **public GitHub portfolio** with clean commit history, tests, and docs

## 6. AI Engineer Roadmap Gaps & Redesign

### Proposed Updated Curriculum (8 weeks)

| Week | New Topic | Rationale |
|------|-----------|-----------|
| 0 | Math & Stats Foundations for AI (new) | Fills the "first principles" gap |
| 1 | Python for Data Science & AI (existing, keep) | Solid foundation |
| 2 | ML Basics & ML Workflow (existing, keep) | Solid foundation |
| 3 | Neural Networks from Scratch + PyTorch (new) | Karpathy-style deep understanding |
| 4 | GenAI Foundations, LLM Working Procedure & Fine-tuning (expanded) | Adds PEFT/LoRA |
| 5 | RAG: Retrieval, Evaluation & Production Patterns (expanded) | Adds evals, hybrid search depth |
| 6 | AI Automation (n8n) + Agent Memory & Multi-Agent Systems (expanded) | Adds memory, observability |
| 7 | MLOps/LLMOps: CI/CD, Monitoring, Cost & Security (new) | Closes production gap |
| 8 | Capstone: Production AI Career Coach + Deployment (existing, expanded) | Portfolio centerpiece |

### Immediate Action Items (this revision cycle)
1. Add `week00_foundations/` (math/stats) and `week_extra_nn_pytorch/` modules — **planned,
   not yet built** (to be scheduled).
2. Add an **evaluation harness** lab to Week 4 (RAG) using `ragas` or a custom rubric.
3. Add a **fine-tuning lab** (LoRA on a small model with `peft`) to Week 3 (GenAI).
4. Add a **Polars/DuckDB** comparison notebook to Week 1 as an "advanced" optional module.
5. Stand up full **open-source project infrastructure** (this commit): CI/CD, pre-commit,
   issue/PR templates, contributing guide, release process — see below.

> Status: This document captures the redesign plan. Curriculum content for Weeks 2+ will be
> built incrementally (one week per session), incorporating the improvements above where
> they fit naturally into existing week scope, with new weeks (0, 3-extra, 7) scheduled as
> additional sessions.
