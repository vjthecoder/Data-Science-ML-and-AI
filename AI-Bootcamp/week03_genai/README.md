# Week 3: GenAI Foundations & LLM Working Procedure

## Learning Objectives
- Understand transformer architecture and attention intuitively and mathematically
- Understand embeddings, tokens, and vector databases
- Write effective prompts (prompt engineering)
- Build basic agents with tool/function calling and understand MCP
- Understand multi-agent systems

## Estimated Duration
20-25 hours

## Prerequisites
- Week 1 Python
- Basic linear algebra (vectors, dot product, matrix multiplication) helpful but not required

## Modules
1. Transformer Architecture — encoder/decoder, self-attention
2. Attention Mechanism — Q/K/V, scaled dot-product attention (math + intuition)
3. Tokens & Embeddings
4. Vector Databases — similarity search basics
5. Prompt Engineering — zero-shot, few-shot, chain-of-thought, system prompts
6. Agents & Tool/Function Calling
7. MCP (Model Context Protocol) — concepts and architecture
8. Multi-Agent Systems — orchestration patterns

## Theory Notes
Each notebook includes diagrams (see `../diagrams/week03_genai/`) and explains
concepts at three levels (child / student / professional), plus math derivations
for attention and embeddings.

## Jupyter Notebooks
- `notebooks/01_transformers_attention.ipynb`
- `notebooks/02_embeddings_tokens.ipynb`
- `notebooks/03_vector_databases.ipynb`
- `notebooks/04_prompt_engineering.ipynb`
- `notebooks/05_tool_function_calling.ipynb`
- `notebooks/06_mcp_overview.ipynb`
- `notebooks/07_multi_agent_systems.ipynb`

## Coding Labs
- `labs/lab1_openai_basics.ipynb` — OpenAI API: chat, function calling
- `labs/lab2_anthropic_basics.ipynb` — Anthropic API: chat, tool use
- `labs/lab3_gemini_basics.ipynb` — Google Gemini API basics
- `labs/lab4_opensource_llm.ipynb` — Local/open-source model via Hugging Face Transformers
- `labs/lab5_simple_agent.ipynb` — Build a simple tool-using agent

## Mini Projects
- Multi-provider "LLM playground" CLI (OpenAI/Anthropic/Gemini/open-source)
- Tool-calling weather + calculator agent
- Two-agent (researcher + writer) pipeline

## Real Industry Examples
- Customer support copilots using function calling to look up orders
- Internal "ask-your-data" agents using tool calling against APIs
- Multi-agent content pipelines (research -> draft -> review)

## Assignments
See `assignments/`

## Interview Questions
See `../interview-prep/week03_genai_questions.md`

## Common Mistakes
- Treating embeddings from different models as comparable
- Overly long prompts with no structure
- Giving agents too many tools without clear descriptions
- Not handling tool-call errors/timeouts in agent loops

## Best Practices
- Use system prompts to set role, constraints, and output format
- Keep tool schemas small, specific, and well-documented
- Cache embeddings; version your embedding model
- Log full agent traces for debugging

## Further Reading
- "Attention Is All You Need" (Vaswani et al., 2017)
- OpenAI, Anthropic, Google Gemini API docs
- Model Context Protocol specification
