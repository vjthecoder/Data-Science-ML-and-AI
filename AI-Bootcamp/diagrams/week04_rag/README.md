# Week 4 Diagrams: RAG — Retrieval Augmented Generation

## 1. Full RAG Pipeline

```mermaid
flowchart TD
    subgraph Indexing[Indexing — offline]
      D[Documents] --> C[Chunk]
      C --> E[Embed]
      E --> DB[(Vector DB + metadata)]
    end
    subgraph Query[Query — online]
      Q[User question] --> QE[Embed]
      QE --> R[Retrieve top-k]
      R --> F[Filter / Rerank]
      F --> P[Build prompt: context + question]
      P --> LLM[LLM]
      LLM --> A[Grounded answer + citations]
    end
    DB --> R
```

## 2. Chunking Strategies

```mermaid
flowchart LR
    T[Document] --> FX[Fixed-size]
    T --> OV[Fixed-size + overlap]
    T --> RC[Recursive: paragraph -> sentence -> word]
    T --> SM[Semantic: split on topic shift]
    FX --> M[Chunks + metadata]
    OV --> M
    RC --> M
    SM --> M
```

## 3. Hybrid Search + Reranking

```mermaid
flowchart TD
    Q[Query] --> V[Vector search top-N]
    Q --> B[BM25 keyword top-N]
    V --> FU[Fuse with RRF]
    B --> FU
    FU --> CE[Cross-encoder rerank]
    CE --> TOP[Precise top-k]
```

## 4. Metadata Filtering (pre-filter)

```mermaid
flowchart LR
    Q[Query + filters] --> PF[Pre-filter by metadata]
    PF --> SUB[Eligible subset]
    SUB --> SS[Semantic search]
    SS --> K[Top-k authorized, fresh, localized]
```

## 5. RAG Evaluation

```mermaid
flowchart TD
    ES[Eval set: Q + relevant ids + ref answer] --> RET[Retrieval metrics: recall@k, precision@k, MRR]
    ES --> GEN[Generation metrics: faithfulness, answer relevance, context relevance]
    RET --> DEC[Decision: ship / iterate]
    GEN --> DEC
```

## 6. PDF Chatbot Architecture

```mermaid
flowchart LR
    U[PDF upload] --> X[Extract text - pypdf]
    X --> CH[Chunk + page metadata]
    CH --> EM[Embed - MiniLM]
    EM --> CR[(Chroma)]
    QN[User question] --> EQ[Embed] --> RT[Retrieve top-k + threshold]
    CR --> RT
    RT --> PR[Prompt + context] --> CL[Claude] --> AN[Answer + source/page citations]
```
