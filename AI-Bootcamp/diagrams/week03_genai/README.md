# Week 3 Diagrams: GenAI Foundations & LLM Working Procedure

## 1. Transformer Block (Decoder-Only)

```mermaid
flowchart TD
    A[Token Embeddings + Positional Encoding] --> B[Masked Multi-Head Self-Attention]
    B --> C[Add & LayerNorm]
    C --> D[Feed-Forward Network]
    D --> E[Add & LayerNorm]
    E --> F[Next Block ... xN]
    F --> G[Linear + Softmax over Vocabulary]
    G --> H[Next-Token Probabilities]
```

## 2. Scaled Dot-Product Attention

```mermaid
flowchart LR
    Q[Query] --> S["scores = QKᵀ / √d_k"]
    K[Key] --> S
    S --> M[Causal Mask: future = -inf]
    M --> SM[Softmax]
    SM --> W[Weights]
    V[Value] --> O["Output = Weights · V"]
    W --> O
```

## 3. Text → Tokens → Embeddings

```mermaid
flowchart LR
    T[Text] -->|BPE tokenizer| TK[Tokens]
    TK -->|embedding lookup| V[Vectors]
    V -->|cosine similarity| R[Semantic comparison / search]
```

## 4. RAG-Style Vector Search Pipeline

```mermaid
flowchart LR
    D[Documents] -->|embed| DV[Doc Vectors + Metadata]
    DV --> DB[(Vector DB: FAISS / Chroma)]
    Q[Query] -->|embed| QV[Query Vector]
    QV -->|k-NN + metadata filter| DB
    DB --> TopK[Top-k Results]
```

## 5. Tool / Function Calling Loop

```mermaid
sequenceDiagram
    participant App
    participant LLM
    App->>LLM: prompt + tool schemas
    LLM-->>App: tool_use (name, input), stop_reason=tool_use
    App->>App: execute function
    App->>LLM: tool_result (matching tool_use_id)
    LLM-->>App: final answer (stop_reason=end_turn)
```

## 6. MCP Architecture

```mermaid
flowchart LR
    subgraph Client[LLM App = MCP Client]
      C[Agent / Desktop / IDE]
    end
    C <-->|MCP: tools/resources/prompts| S1[MCP Server: files]
    C <-->|MCP| S2[MCP Server: GitHub]
    C <-->|MCP| S3[MCP Server: database]
```

## 7. Multi-Agent Patterns

```mermaid
flowchart TD
    subgraph Pipeline
      R[Researcher] --> W[Writer] --> Rev[Reviewer]
    end
    subgraph FanOut[Orchestrator-Worker]
      O[Orchestrator] --> WA[Worker A]
      O --> WB[Worker B]
      O --> WC[Worker C]
      WA --> AG[Aggregator]
      WB --> AG
      WC --> AG
    end
```
