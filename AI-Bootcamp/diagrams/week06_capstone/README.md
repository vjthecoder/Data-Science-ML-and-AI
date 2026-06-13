# Week 6 Diagrams: AI Career Coach (Capstone)

## 1. Application Architecture

```mermaid
flowchart TD
    subgraph Clients
      UI[Streamlit UI]
      API[FastAPI /docs]
    end
    UI --> AG[agent.coach action]
    API --> AG
    AG --> RP[resume_parser: extract skills, skill_gap]
    AG --> RAG[rag: KnowledgeBase.retrieve]
    RAG --> CTX[Grounding context]
    CTX --> LLM[Claude claude-opus-4-8]
    RP --> LLM
    LLM --> OUT[Analysis / gaps / questions / roadmap]
```

## 2. Feature → Module Map

```mermaid
flowchart LR
    F1[Resume Analysis] --> A[agent.analyze_resume]
    F2[Skill Gap] --> B[agent.detect_skill_gap]
    F3[Interview Questions] --> C[agent.generate_interview_questions]
    F4[Learning Path] --> D[agent.generate_learning_path]
    A --> R[(RAG KB)]
    B --> P[resume_parser]
    C --> R
    D --> R
```

## 3. Request Flow (Skill Gap example)

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit/FastAPI
    participant AG as agent
    participant RP as resume_parser
    participant LLM as Claude
    U->>UI: resume + job description
    UI->>AG: detect_skill_gap()
    AG->>RP: extract_skills + skill_gap (deterministic)
    AG->>LLM: advice grounded in gap + RAG context
    LLM-->>AG: advice text
    AG-->>UI: {matched, missing, coverage, advice}
    UI-->>U: metrics + advice
```

## 4. Deployment Topology

```mermaid
flowchart LR
    GH[GitHub repo] --> CI[CI: lint + test + build]
    CI --> IMG[Docker image]
    IMG --> RUN[Render / Railway / Cloud Run / AWS]
    SEC[(Secret manager: ANTHROPIC_API_KEY)] -. injected at runtime .-> RUN
    RUN --> USERS[Public HTTPS URL]
```

## 5. GitHub Packaging

```mermaid
flowchart TD
    REPO[Repo] --> RM[README + architecture + demo]
    REPO --> REQ[requirements.txt + Dockerfile]
    REPO --> ENV[.env.example - no secrets]
    REPO --> T[tests + CI green]
    REPO --> LIC[LICENSE]
```
