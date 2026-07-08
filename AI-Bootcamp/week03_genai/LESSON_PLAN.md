# Week 3 Lesson Plan: GenAI Foundations & LLM Working Procedure

**Total Duration:** ~20-25 hours over 5-6 days

| Day | Topics | Notebook(s) | Duration | Deliverable |
|-----|--------|-------------|----------|-------------|
| 1 | Transformers & Attention | `01_transformers_attention.py` | 3h | Assignment 1 |
| 2 | Tokens, Embeddings & Vector DBs | `02_embeddings_tokens.py`, `03_vector_databases.py` | 4h | Assignments 2-3 |
| 3 | Prompt Engineering + Provider Labs | `04_prompt_engineering.py`, `labs/lab1-3` | 4h | Assignment 4, Labs 1-3 |
| 4 | Tool/Function Calling + Open-Source LLMs | `05_tool_function_calling.py`, `labs/lab4` | 4h | Assignment 5, Lab 4 |
| 5 | MCP + Simple Agent | `06_mcp_overview.py`, `labs/lab5_simple_agent.py` | 4h | Assignment 6, Lab 5 |
| 6 | Multi-Agent Systems | `07_multi_agent_systems.py` | 3-4h | Assignment 7 |

## Prerequisites Check (Day 0)
```bash
pip install -r AI-Bootcamp/requirements.txt
# For provider labs (optional, needs keys):
pip install openai anthropic google-generativeai
# Set keys as environment variables — never hardcode:
export ANTHROPIC_API_KEY=...   # OPENAI_API_KEY, GOOGLE_API_KEY similarly
```
> All concept notebooks include **offline-safe** demos, so the theory and core exercises run
> without any API key. Provider labs require the relevant key (or use the offline fallbacks).

## Model Note
Examples default to `claude-opus-4-8` (Anthropic's capable default). For the most demanding
reasoning, `claude-fable-5` is Anthropic's most capable model. Always read keys from the
environment.

## Session Format (per day)
Warm-up review → theory walkthrough (3 levels) → live coding of the offline demo → guided
exercise → lab/assignment → wrap-up (common mistakes + best practices).

## Assessment
- 7 assignments — see `assignments/week03_assignments.md`
- 5 labs (OpenAI, Anthropic, Gemini, open-source, simple agent) — see `labs/`
- End-of-week quiz from `../interview-prep/week03_genai_questions.md`

## Success Criteria
By the end of Week 3, students can:
- Explain transformers, attention, tokens, and embeddings both intuitively and mathematically
- Use vector databases (FAISS/Chroma) for semantic search
- Write effective, eval-tested prompts and request structured outputs
- Implement tool/function calling and a simple tool-using agent
- Explain MCP and build a minimal MCP server/client
- Design a basic multi-agent pipeline and judge when it's worth the cost
