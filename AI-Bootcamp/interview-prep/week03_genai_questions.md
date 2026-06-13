# Week 3 Interview Questions: GenAI Foundations & LLM Working Procedure

## Transformers & Attention
1. Explain self-attention in your own words. What are Q, K, and V?
2. Why is attention scaled by `1/√d_k`?
3. What is the difference between encoder (bidirectional) and decoder (causal) attention?
4. Why is a causal mask needed for autoregressive text generation?
5. What is multi-head attention, and why use multiple heads instead of one?
6. Why is attention O(n²) in sequence length, and how does that affect context windows?
7. What do positional encodings do, and why are they necessary?

## Tokens & Embeddings
8. What is tokenization, and why do models use sub-word (BPE) tokens?
9. Why do token counts differ between OpenAI and Anthropic models?
10. What is an embedding? Why are similar concepts close in embedding space?
11. Why must you normalize vectors before computing cosine similarity?
12. Why can't you compare embeddings produced by two different models?
13. How do token counts affect cost and context-window limits in production?

## Vector Databases
14. What problem does a vector database solve that a SQL database doesn't?
15. Explain approximate nearest neighbor (ANN) search. Why not always use exact search?
16. Compare HNSW and IVF indexes. What trade-offs do they make?
17. What is recall@k, and how would you measure it for an ANN index?
18. Why attach metadata to vectors? Give two uses.
19. When would you choose FAISS vs Chroma vs a managed service like Pinecone?

## Prompt Engineering
20. Contrast zero-shot, few-shot, and chain-of-thought prompting.
21. What goes in a system prompt vs a user message?
22. Why prefer structured outputs (JSON schema) over parsing free text?
23. What is eval-driven prompt development, and why does it matter in production?
24. Why can overly aggressive "CRITICAL/MUST" instructions hurt on modern models?

## Tool / Function Calling
25. Walk through the tool-calling loop end to end.
26. How does the model decide which tool to call? What makes a good tool description?
27. How should tool execution errors be handled so the model can recover?
28. Why must side-effecting tools (email, DB writes) be gated or validated?
29. What's the difference between a "tool runner" and a manual agentic loop?

## MCP (Model Context Protocol)
30. What is MCP, and what problem does it solve?
31. Name the three MCP primitives (tools, resources, prompts) and give an example of each.
32. How does MCP differ from writing a one-off function-calling integration?
33. What's the security benefit of keeping credentials in the MCP server/host?
34. What transports does MCP use, and when would you use each?

## Multi-Agent Systems
35. Describe orchestrator-worker, pipeline, and parallel fan-out patterns.
36. When does a multi-agent system beat a single well-prompted agent?
37. What are the downsides of multi-agent designs (cost, latency, debugging)?
38. How do agents communicate and pass results in a pipeline?
39. Why is asynchronous delegation often better than spawn-and-block for long sub-agents?

## Scenario / System Design
40. Design a customer-support assistant that answers from a knowledge base and can look up
    order status. Which Week 3 concepts (embeddings, vector DB, tools, agents) do you use, and
    how do they fit together?
41. Your LLM app's costs are too high. List five levers you'd pull (tokens, model choice,
    caching, structured outputs, retrieval) and the trade-offs of each.
42. A tool-using agent occasionally loops forever. What are the likely causes and your fixes?
43. How would you evaluate whether a new prompt is actually better than the old one before
    shipping it?
