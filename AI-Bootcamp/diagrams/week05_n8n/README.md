# Week 5 Diagrams: AI Automation with n8n

## 1. n8n Mental Model

```mermaid
flowchart LR
    TR[Trigger: manual / webhook / schedule / IMAP / chat] --> N1[Node transforms data item-by-item]
    N1 --> N2[Node: LLM / HTTP / DB]
    N2 --> N3[Branch: IF / Switch]
    N3 --> OUT[Action: send / store / respond]
    CR[(Credential store - encrypted)] -. supplies secrets .-> N2
```

## 2. Email Automation

```mermaid
flowchart LR
    IMAP[IMAP Trigger] --> CL[Claude: classify]
    CL --> SW{Switch: category}
    SW -->|support| RE[Email Send: auto-reply]
    SW -->|sales| CRM[Create lead]
    SW -->|spam/other| NO[No-op / log]
```

## 3. Lead Qualification

```mermaid
flowchart LR
    WH[Webhook: form] --> SC[Claude: score JSON]
    SC --> P[Code: parse score]
    P --> IFn{score >= 70?}
    IFn -->|yes| AT[Airtable: create]
    IFn -->|no| RSP[Respond]
    AT --> RSP
```

## 4. AI Agent (tools + memory)

```mermaid
flowchart TD
    CT[Chat Trigger] --> AG[AI Agent]
    LM[Anthropic Chat Model] -. ai_languageModel .-> AG
    MEM[Window Memory] -. ai_memory .-> AG
    TOOL[Calculator / HTTP Tool] -. ai_tool .-> AG
    AG --> REPLY[Reply]
```

## 5. CRM Automation (scheduled)

```mermaid
flowchart LR
    SCH[Schedule every 6h] --> GET[Airtable: new contacts]
    GET --> EN[Claude: enrich]
    EN --> UP[HubSpot: update]
```

## 6. Multi-Agent Content Pipeline

```mermaid
flowchart LR
    WH[Webhook: topic] --> R[Researcher]
    R --> W[Writer]
    W --> Rev[Reviewer]
    Rev --> RS[Respond: final]
```
